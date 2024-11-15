from marshmallow import Schema, fields


class PendingUserOutput(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    role = fields.Str(dump_only=True)


class PendingUserListOutput(Schema):
    pending_users = fields.List(fields.Nested(PendingUserOutput))
