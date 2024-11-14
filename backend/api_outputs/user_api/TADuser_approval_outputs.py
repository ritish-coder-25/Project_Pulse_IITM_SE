# api_outputs/user_approval_outputs.py
from marshmallow import Schema, fields


class UserApprovalResult(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)


class UserApprovalOutput(Schema):
    message = fields.Str()
    results = fields.List(fields.Nested(UserApprovalResult))
