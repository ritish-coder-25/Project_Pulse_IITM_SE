from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    student_email = fields.Email(required=True)
    user_type = fields.Str(required=True)
    marker = fields.Str()

class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    team_name = fields.Str(required=True)
    github_repo_url = fields.Url(required=True)
    team_lead_id = fields.Int(required=True)
    project_id = fields.Int(required=True)

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    project_name = fields.Str(required=True)
    description = fields.Str()

class MilestoneSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    due_date = fields.Date()

class MilestoneStatusSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str(required=True)
    milestone_id = fields.Int(required=True)

class CommitSchema(Schema):
    id = fields.Int(dump_only=True)
    commit_hash = fields.Str(required=True)
    commit_message = fields.Str(required=True)
    user_id = fields.Int(required=True)

class CommonErrorSchema(Schema):
    errorCode = fields.Str(required=True)
    message = fields.Str(required=True)

class CommonErrorErrorSchemaFatal(CommonErrorSchema):
    error = fields.Str(required=True)


class MilestoneDeadlineSchema(Schema):
    milestone_name = fields.String(
        required=True, description="Name of the milestone")
    milestone_description = fields.String(
        required=True, description="Description of the milestone")
    end_date = fields.String(
        required=True, description="Formatted end date of the milestone")


class SubmitProjectResponseSchema(Schema):
    message = fields.String(required=True, description="Response message")
    file_path = fields.String(
        required=True, description="Path where the file is saved")
