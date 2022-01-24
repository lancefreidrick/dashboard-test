# pylint: disable=global-statement
from os import path
import uuid
from urllib.parse import urlparse, ParseResult
import boto3

from server.config.logger import log
from server.models.merchant_model import Merchant
from server.models.settlement_model import SettlementFile

__bucket = None
__client = None

EXPIRES_AT = 3600

class PresignedUrl:
    def __init__(
            self,
            url: str,
            bucket: str=None,
            directory: str=None,
            unique_identifier: str=None):
        self.url = url
        self.bucket_name = bucket
        self.file_directory = directory
        self.unique_identifier = unique_identifier

    def parse_url(self) -> ParseResult:
        return urlparse(self.url)


def setup(key: str, secret: str, bucket: str, region: str):
    global __client, __bucket
    __bucket = bucket
    __client = boto3.client(
        service_name='s3',
        aws_access_key_id=key,
        aws_secret_access_key=secret,
        region_name=region)
    log.info(f's3:      Setting up AWS s3 for {bucket} bucket in {region}')


def get_presigned_upload_url(merchant: Merchant, filename: str, metadata: dict) -> PresignedUrl:
    """
    Returns (Presigned Url: str, File Directory: str, Unique Identifier: str)
    """
    global __bucket, __client

    if not merchant or not filename:
        return None, None, None

    unique_identifier = uuid.uuid4()
    file_directory = f'settlement-reports/{merchant.merchant_code}/{unique_identifier}'

    presigned_url = __client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': __bucket,
            'Key': f'{file_directory}/{filename}',
            'ContentType': metadata.get('contentType'),
            'ContentLength': metadata.get('contentLength')
        },
        ExpiresIn=EXPIRES_AT)
    return PresignedUrl(
        url=presigned_url,
        bucket=__bucket,
        directory=file_directory,
        unique_identifier=unique_identifier)


def get_presigned_download_url(file: SettlementFile) -> PresignedUrl:
    global __bucket, __client

    if not file:
        return None
    if not file.s3_file_directory or not file.s3_file_name:
        return None

    key = path.join(file.s3_file_directory, file.s3_file_name)

    presigned_url = __client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': file.s3_bucket_name or __bucket,
            'Key': key
        },
        ExpiresIn=EXPIRES_AT)

    return PresignedUrl(
        url=presigned_url,
        bucket=file.s3_bucket_name,
        directory=file.s3_file_directory,
        unique_identifier=file.unique_identifier)
