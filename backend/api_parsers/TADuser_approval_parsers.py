from marshmallow import Schema, fields, validate


class UserApprovalParser(Schema):
    user_id = fields.Int(required=True)
    approval_status = fields.Str(
        required=True, validate=validate.OneOf(["Approved", "Declined"])
    )
    user_type = fields.Str(required=True)


class ApproveUsersRequest(Schema):
    users = fields.List(
        fields.Nested(UserApprovalParser),
        required=True,
        validate=validate.Length(min=1),
    )
