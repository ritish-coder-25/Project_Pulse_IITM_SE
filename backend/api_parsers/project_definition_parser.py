from marshmallow import Schema, fields, validate


class CreateProjectSchema(Schema):
    # Project name is required and should be a non-empty string
    name = fields.Str(required=True, validate=validate.Length(min=1), description="The name of the project.")
    
    # Project statement is required and should be a non-empty string
    statement = fields.Str(required=True, validate=validate.Length(min=1), description="The statement of the project.")
    
    # Document URL is required and should be a valid URL
    document_url = fields.Str(required=True, validate=validate.URL(), description="URL for the project document.")
