from marshmallow import Schema, fields, validate


class UserApprovalParser(Schema):
    user_id = fields.Int(required=True)
    approval_status = fields.Str(
        required=True, validate=validate.OneOf(["Active", "Decline"])
    )
    user_type = fields.Str(required=True)


class ApproveUsersRequest(Schema):
    users = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Str()),
        required=True,
        validate=validate.Length(min=1),
    )
