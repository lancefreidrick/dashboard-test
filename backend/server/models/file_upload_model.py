from marshmallow import Schema, fields


class FileUploadSchema(Schema):
    """
    Used for return JSON-structured values on the API endpoints
    """
    id = fields.Str()
    settlementId = fields.Str(attribute='settlement_id')
    directory = fields.Str(attribute='directory')
    filename = fields.Str(attribute='filename')
    contentType = fields.Str(attribute='content_type')
    createdAt = fields.DateTime(attribute='created_at', format='iso')

    class Meta:
        fields = ('id', 'settlementId', 'directory', 'filename', 'contentType', 'createdAt')
        ordered = True


class FileUpload():
    def __init__(self):
        self.id = None
        self.settlement_id = None
        self.directory = None
        self.filename = None
        self.content_type = None
        self.created_at = None

    def serialize(self):
        return FileUploadSchema().dump(self)

    @staticmethod
    def map(data: dict):
        """
        @returns FileUpload
        """
        fileupload = FileUpload()
        fileupload.id = data.get('settlement_file_id')
        fileupload.settlement_id = data.get('settlement_id')
        fileupload.directory = data.get('s3_file_directory')
        fileupload.filename = data.get('s3_file_name')
        fileupload.content_type = data.get('s3_file_type')
        fileupload.created_at = data.get('created_at')
        return fileupload
