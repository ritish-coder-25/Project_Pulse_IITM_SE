# schemas.py
from marshmallow import Schema, fields, validate


class PutTeamSchema(Schema):
    team_id = fields.Int(required=True)
    user_ids = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))


class CreateTeamSchema(Schema):
    team = fields.Str(required=True, validate=validate.Length(min=1))
    github_repo_url = fields.Str(required=True, validate=validate.Length(min=1))
    user_ids = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))
