from marshmallow import Schema, fields

class CommitQueryParamsSchema(Schema):
    since = fields.String(required=True, description="Start datetime for commit retrieval in ISO format.")
    until = fields.String(required=True, description="End datetime for commit retrieval in ISO format.")
    repo_owner = fields.String(required=False, description="Owner of the repository.", allow_none=True)
    repo_name = fields.String(required=False, description="Name of the repository.", allow_none=True)
    team_id = fields.Integer(required=True, description="Team ID for the repository.")
