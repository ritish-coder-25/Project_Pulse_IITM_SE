from marshmallow import Schema, fields


class MilestoneCompletionOutput(Schema):
    team = fields.Str(dump_only=True)


class MilestoneCompletionsResponse(Schema):
    completions = fields.List(fields.Nested(MilestoneCompletionOutput), dump_only=True)
