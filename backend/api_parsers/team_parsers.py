# schemas.py
from marshmallow import Schema, fields, validate


class PutTeamSchema(Schema):
    team_id = fields.Int(required=True)
    emails = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))


class CreateTeamSchema(Schema):
    team = fields.Str(required=True, validate=validate.Length(min=1))
    github_repo_url = fields.Str(required=True, validate=validate.Length(min=1))
    emails = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
