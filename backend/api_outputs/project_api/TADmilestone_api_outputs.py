from marshmallow import Schema, fields


class MilestoneCompletionOutput(Schema):
    team = fields.Str(dump_only=True)


class MilestoneCompletionsResponse(Schema):
    completions = fields.List(fields.Nested(MilestoneCompletionOutput), dump_only=True)


class ProjectOutput(Schema):
    project_id = fields.Int(dump_only=True)  # Project ID field
    name = fields.Str(dump_only=True)  # Project name
    statement = fields.Str(dump_only=True)  # Project statement
    document_url = fields.Str(dump_only=True)  # Document URL


class ProjectCreationResponse(Schema):
    message = fields.Str()  # Response message
    project = fields.Nested(ProjectOutput, dump_only=True)  # Project details

class CommonErrorSchema(Schema):
    errorCode = fields.Str(required=True)
    message = fields.Str(required=True)

class CommonErrorErrorSchemaFatal(CommonErrorSchema):
    error = fields.Str(required=True)


class MilestoneOutput(Schema):
    milestone_id = fields.Int(dump_only=True)  # Milestone ID
    milestone_name = fields.Str(dump_only=True)  # Milestone name
    milestone_description = fields.Str(dump_only=True)  # Milestone description
    start_date = fields.Date(dump_only=True)  # Start date
    end_date = fields.Date(dump_only=True)  # End date
    max_marks = fields.Float(dump_only=True)  # Maximum marks
    project_id = fields.Int(dump_only=True)


class MilestoneCreationResponse(Schema):
    message = fields.Str()  # Response message


class MilestoneUpdateResponse(Schema):
    message = fields.Str()  # Response message


class MilestoneDeletionResponse(Schema):
    message = fields.Str()  # Response message


class MilestoneListResponse(Schema):
    milestones = fields.List(
        fields.Nested(MilestoneOutput), dump_only=True
    )  # List of milestones
