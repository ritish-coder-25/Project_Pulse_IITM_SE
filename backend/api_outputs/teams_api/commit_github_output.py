from marshmallow import Schema, fields, validate, post_load

class FileChangeSchema(Schema):
    filename = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["added", "modified", "removed"]))
    additions = fields.Int(required=True)
    deletions = fields.Int(required=True)
    total_changes = fields.Int(required=True)
    changes_str = fields.Str(required=True)
    code_changes = fields.Str(allow_none=True)

class CommitDetailSchema(Schema):
    commit_sha = fields.Str(required=True)
    message = fields.Str(required=True)
    date = fields.Str(required=True, validate=validate.Regexp(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"))  # ISO 8601
    file_changes = fields.List(fields.Nested(FileChangeSchema), required=True)

class CommitUserSchema(Schema):
    total_commits = fields.Int(required=True)
    commit_details = fields.List(fields.Nested(CommitDetailSchema), required=True)

class CommitsResponseSchema(Schema):
    users = fields.Dict(keys=fields.Str(), values=fields.Nested(CommitUserSchema), required=True)
