from server.config import database
from server.models.file_upload_model import FileUpload


def create_settlement_file(directory: str, filename: str, content_type: str, settlement_id: int) -> (bool, str):
    db_params = [
        settlement_id,
        directory,
        filename,
        content_type
    ]
    result = database.func('invoicing.create_settlement_file', db_params)
    if result[0]['status'] == 'success':
        return (True, result[0]['created_settlement_file_id'])
    return (False, result[0]['message'])


def find_settlement_file_by_id(file_id: int):
    db_params = [file_id]
    queried_file_upload = database.func('invoicing.find_settlement_file_by_id', db_params)
    if not queried_file_upload:
        return None
    return FileUpload.map(queried_file_upload[0])


def delete_settlement_file_by_id(settlement_file_id: int):
    db_params = [settlement_file_id]
    result = database.func('invoicing.delete_settlement_file_by_id', db_params)
    return (result[0]['status'] == 'success', result[0]['message'])
