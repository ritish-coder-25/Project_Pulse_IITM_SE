from marshmallow import Schema, fields


class UploadOutput(Schema):
    team = fields.Str(dump_only=True)


class UploadsResponse(Schema):
    uploads = fields.List(fields.Nested(UploadOutput), dump_only=True)
