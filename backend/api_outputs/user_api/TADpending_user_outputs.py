from marshmallow import Schema, fields


# api_outputs/pending_user_outputs.py
class PendingUserOutput(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)


class PendingUserListOutput(Schema):
    pending_users = fields.List(fields.Nested(PendingUserOutput))
    message = fields.Str()
