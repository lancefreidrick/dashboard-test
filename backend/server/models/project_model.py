""" server.models.project_model.py """
import re
from datetime import datetime
from marshmallow import Schema, ValidationError, validate, fields as _fields


class ProjectMetadataItemSchema(Schema):
    name = _fields.Str(required=True, validate=validate.Length(min=1, max=50))
    text = _fields.Str(required=True, validate=validate.Length(min=1, max=50))
    value = _fields.Raw(required=True)


class ProjectMetadataSchema(Schema):
    fields = _fields.List(_fields.Nested(ProjectMetadataItemSchema()), required=True)


class ProjectSchema(Schema):
    id = _fields.Int(attribute='project_id')
    code = _fields.Str(attribute='project_code')
    key = _fields.Str(attribute='project_key')
    name = _fields.Str(attribute='name')
    category = _fields.Str(attribute='category')
    description = _fields.Str(attribute='description')
    isActive = _fields.Bool(attribute='is_active')
    isEnabled = _fields.Bool(attribute='is_enabled')
    projectFields = _fields.Nested(ProjectMetadataSchema(), attribute='project_fields')
    modifiedAt = _fields.DateTime(attribute='modified_at', format='iso')

    class Meta:
        fields = (
            'id', 'code', 'key',
            'merchantCode', 'name',
            'category', 'description',
            'projectFields', 'isActive',
            'isEnabled', 'modifiedAt'
        )
        ordered = True


class SubmittedProjectSchema(Schema):
    name = _fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = _fields.Str(required=False, allow_none=True, validate=validate.Length(min=0, max=50))
    description = _fields.Str(required=False, allow_none=True, validate=validate.Length(min=0, max=250))


class Project:
    def __init__(self):
        self.project_id: int = None
        self.project_code: str = None
        self.merchant_code: str = None
        self.merchant_id: int = None
        self.project_key: str = None
        self.name: str = None
        self.category: str = None
        self.description: str = None
        self.source: str = None
        self.project_fields: dict = None
        self.is_active: bool = False
        self.is_enabled: bool = False
        self.modified_at: datetime = None

    def serialize(self):
        return ProjectSchema().dump(self)

    def __eq__(self, other):
        if not isinstance(other, Project):
            return False
        return self.name == other.name

    def  __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'#{self.project_id}: {self.displayed_name}'

    def __repr__(self):
        return f'Project({self.project_id}, {self.displayed_name})'

    def generate_key(self, prefix: str) -> str:
        lowered_name = re.sub('[^a-zA-Z0-9\\-]', '', self.name.lower())
        return f'{prefix}-{lowered_name}'

    @property
    def displayed_name(self):
        if self.category and self.category != 'default':
            return f'{self.category} - {self.name}'

        return self.name

    @staticmethod
    def validate_submitted_info(data: dict):
        try:
            info = SubmittedProjectSchema().load(data)
            return True, info
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def validate_metadata_fields(data: list):
        try:
            metadata = [ProjectMetadataItemSchema().load(m) for m in data]
            return True, metadata

        except ValidationError as verr:
            return False, verr

    @staticmethod
    def map(data):
        if data is None:
            return None

        project = Project()
        project.project_id = data.get('merchant_project_id')
        project.project_code = data.get('project_code')
        project.merchant_code = data.get('merchant_code')
        project.merchant_id = data.get('merchant_id')
        project.name = data.get('project_name')
        project.category = data.get('project_category')
        project.description = data.get('project_description')
        project.source = data.get('project_source')
        project.project_fields = data.get('project_fields')
        project.project_key = data.get('project_key')
        project.is_active = data.get('is_active')
        project.is_enabled = data.get('is_enabled')
        project.modified_at = data.get('updated_at')

        return project
