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
