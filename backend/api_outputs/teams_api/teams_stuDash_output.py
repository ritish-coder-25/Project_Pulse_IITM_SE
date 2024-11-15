from marshmallow import Schema, fields

class MemberSchema(Schema):
    name = fields.String(required=True, description="Member's full name")
    email = fields.Email(required=True, description="Member's email address")
    commit_count = fields.Integer(required=True, description="Number of commits by the member")

class MilestoneSchema(Schema):
    milestone_name = fields.String(required=True, description="Name of the milestone")
    milestone_status = fields.String(required=True, description="Status of the milestone (e.g., Evaluated, Completed, Pending, Missed)")
    end_date = fields.DateTime(required=True, description="End date of the milestone")

class StuDashTeamSchema(Schema):
    team_name = fields.String(required=True, description="Name of the team")
    team_score = fields.Float(required=True, description="Total score for the team")
    members = fields.List(fields.Nested(MemberSchema), required=True, description="List of team members")
    milestones = fields.List(fields.Nested(MilestoneSchema), required=True, description="List of milestones with details")


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
