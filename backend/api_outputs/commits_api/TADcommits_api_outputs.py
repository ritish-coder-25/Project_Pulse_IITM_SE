from marshmallow import Schema, fields


class CommitOutput(Schema):
    team = fields.Str(dump_only=True)


class CommitsResponse(Schema):
    message = fields.Str()
    commits = fields.List(fields.Nested(CommitOutput), dump_only=True)
