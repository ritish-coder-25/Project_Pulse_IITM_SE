from marshmallow import Schema, fields

class CommitQueryParamsSchema(Schema):
    since = fields.String(required=True, description="Start datetime for commit retrieval in ISO format.")
    until = fields.String(required=True, description="End datetime for commit retrieval in ISO format.")
    repo_owner = fields.String(required=True, description="Owner of the repository.")
    repo_name = fields.String(required=True, description="Name of the repository.")
