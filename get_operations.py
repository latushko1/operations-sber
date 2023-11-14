import re
import textwrap
import json

from jinja2 import Template

render_template = Template(
    """
    {{ date }} {{ description }}
    {{ from_operation_type|default('Пустое значение для "from"', true) }} {{from_operation_number}} -> Счет {{ to }}
    {{ operation_amount }} {{ operation_currency }}
    """
)


def get_operation(operation):
    from_operation_type = ''
    from_operation_number = ''
    data_operation = operation['date'].split("T")[0]
    type_operation = operation['description']
    if 'from' in operation:
        from_operation_parts = operation['from'].split(" ")
        from_operation_number = from_operation_parts[-1]
        from_operation_type = " ".join(from_operation_parts[:-1])

        from_operation_number = textwrap.wrap(from_operation_number, 4)
        for index, fragment in enumerate(from_operation_number):
            if index == 1:
                from_operation_number[index] = re.sub(r'.{2}$', '**', fragment)
            elif index == 2:
                from_operation_number[index] = re.sub(r'.{4}$', '****', fragment)
        from_operation_number = " ".join(from_operation_number)

    to_operation = operation['to'].split(" ")[1][-4:]
    operation_amount = operation['operationAmount']['amount']
    operation_currency = operation['operationAmount']['currency']['name']

    return render_template.render(date=data_operation, description=type_operation,
                                  from_operation_type=from_operation_type,
                                  from_operation_number=from_operation_number, to=to_operation,
                                  operation_amount=operation_amount, operation_currency=operation_currency)


if __name__ == "__main__":
    with open("operations.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    data = sorted(data, key=lambda x: x.get("date", ''), reverse=True)

    for idx, item in enumerate(data):
        if item['state'] == 'EXECUTED':
            print(get_operation(item))
            if idx == 5:
                break

    # print(get_operation(data))
