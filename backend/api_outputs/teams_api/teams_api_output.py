from marshmallow import Schema, fields
from models import User, Team, Project, Milestone, MilestoneStatus, Commit

class TeamsCreateOutput(Schema):
    team_id = fields.Int(dump_only=True)
    message = fields.Str()

class TeamsDeleteOutput(Schema):
    message = fields.Str()