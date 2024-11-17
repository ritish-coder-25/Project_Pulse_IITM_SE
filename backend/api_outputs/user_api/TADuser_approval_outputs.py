from marshmallow import Schema, fields


class UserApprovalResult(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)


class UserApprovalOutput(Schema):
    results = fields.List(fields.Nested(UserApprovalResult))
