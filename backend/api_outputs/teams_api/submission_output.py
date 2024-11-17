from marshmallow import Schema, fields
from models import User, Team, Project, Milestone, MilestoneStatus, Commit, File



class DocumentListSchema(Schema):
    documents = fields.List(fields.Dict())

class FileDownloadSchema(Schema):
    file = fields.Raw(description="The downloaded file")