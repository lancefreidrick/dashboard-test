""" helper.py """
import re

transaction_status = {
    'INC': 1,
    'SUCCESS': 2,
    'FAIL': 3,
    'ONGOING': 4,
    'FOR REVIEW': 5,
    'DECLINED': 6,
    'CANCELLED': 7,
    'DONE': 8,
    'PENDING': 9,
}

invoice_status = {
    'PAID': 1,
    'SCHED': 2,
    'FAIL': 3,
    'CANCELLED': 4,
    'SETTLED': 5,
    'REFUNDED': 6,
    'PENDING': 7,
    'DISPUTED': 8
}

def get_id_as_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return -1

def get_proper_label(key: str) -> str:
    if not key:
        return None
    pattern = re.compile('([A-Z])', re.A)
    first_char = key[0].upper()
    replaced_chars = pattern.sub(r' \1', key)[1:]
    return f'{first_char}{replaced_chars}'

def get_fields_as_dict(custom_fields: dict) -> dict:
    result = {}
    if isinstance(custom_fields, list):
        for item in custom_fields:
            result[item['name']] = {
                'label': item['text'],
                'value': item['value']
            }
    elif isinstance(custom_fields, dict):
        for key in custom_fields:
            sub_fields = custom_fields[key]
            if isinstance(sub_fields, list):
                for item in sub_fields:
                    result[item['name']] = {
                        'label': item['text'],
                        'value': item['value']
                    }
            elif isinstance(sub_fields, dict):
                for fkey in sub_fields:
                    result[fkey] = {
                        'label': get_proper_label(fkey),
                        'value': sub_fields[fkey]
                    }
    return result

def transform_key_to_name(key: str) -> str:
    if not key:
        return None

    name = key[0].upper()
    for character in key[1:]:
        if character.isupper():
            name += ' ' + character.lower()
        else:
            name += character.lower()
    return name

def transform_dict_to_list(data: dict):
    return [
        {
            'value': data[key],
            'name': key,
            'text': transform_key_to_name(key)
        } for key in data or {}
    ]

def map_transaction_status(status: str):
    return [
        transaction_status.get(i) for i in status.split(',') if i in transaction_status
    ] if status and isinstance(status, str) else []

def map_invoice_status(status: str):
    return [
        invoice_status.get(i) for i in status.split(',') if i in invoice_status
    ] if status and isinstance(status, str) else []
