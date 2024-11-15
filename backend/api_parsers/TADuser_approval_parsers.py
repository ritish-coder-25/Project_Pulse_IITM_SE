# api_parsers/user_approval_parser.py
from marshmallow import Schema, fields, validate


class UserApprovalParser(Schema):
    id = fields.Int(required=True)
    approved = fields.Bool(required=False)
    rejected = fields.Bool(required=False)
    role = fields.Str(
        missing="Student",
        validate=validate.OneOf(["TA", "Admin", "Instructor", "Developer", "Student"]),
    )


class ApproveUsersRequest(Schema):
    users = fields.List(
        fields.Nested(UserApprovalParser),
        required=True,
        validate=validate.Length(min=1),
    )
