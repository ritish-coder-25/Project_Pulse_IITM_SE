from marshmallow import Schema, fields
from models import User, Team, Project, Milestone, MilestoneStatus, Commit, File


class DocumentSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    team = fields.Str(required=True)
    milestone = fields.Str(required=True)

class DocumentListSchema(Schema):
    documents = fields.List(fields.Nested(DocumentSchema))

class FileDownloadSchema(Schema):
    file = fields.Raw(description="The downloaded file")