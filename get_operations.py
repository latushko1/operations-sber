import re
import textwrap
import json
from datetime import datetime

def format_operation(operation):
    from_operation_type = ''
    from_operation_number = ''
    data_operation = datetime.strptime(operation['date'].split("T")[0], "%Y-%m-%d").strftime("%d.%m.%Y")
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

    if 'Счет' in operation['to']:
        to_operation = '**' + operation['to'].split(" ")[1][-4:]
    else:
        to_operation = operation['to']

    operation_amount = operation['operationAmount']['amount']
    operation_currency = operation['operationAmount']['currency']['name']

    result = f"""
{data_operation} {type_operation}
{from_operation_type or 'Пустое значение для "from"'} {from_operation_number} -> {to_operation}
{operation_amount} {operation_currency}
"""
    return result.strip()


if __name__ == "__main__":
    try:
        with open(r"path_to_operation_file", 'r', encoding='utf-8') as file:
            operations = json.load(file)
    except FileNotFoundError:
        print("Файл операциями не найден.")
    else:
        data = sorted(operations, key=lambda x: x.get("date", ''), reverse=True)
        executed_operations = [item for item in data if item.get('state') == 'EXECUTED']

        for idx, item in enumerate(executed_operations[:5]):
            print(format_operation(item)+ "\n")
