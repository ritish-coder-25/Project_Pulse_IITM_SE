from marshmallow import Schema, fields

class MilestoneDetails(Schema):
    milestone_id = fields.Int()
    project_id = fields.Int()
    milestone_name = fields.Str()
    milestone_description = fields.Str()
    max_marks = fields.Float()
    end_date = fields.DateTime()
    start_date = fields.DateTime()

class TeamAggDetails(Schema):
    team_id = fields.Int()
    team_name = fields.Str()
    commits = fields.Int()
    score = fields.Float()
    total_score = fields.Float()
    milestones_completed = fields.Int()
    milestones_missed = fields.Int()


class TADashboardTeamsGetOutput(Schema):
    milestones = fields.Nested(MilestoneDetails, many=True)
    teams = fields.Nested(TeamAggDetails, many=True)


class MemberCommitsDetails(Schema):
    name = fields.Str()
    email = fields.Str()
    commits = fields.Int()


class MilestoneStatusDetails(Schema):
    milestonestatus_id = fields.Int()
    milestone_id = fields.Int()
    team_id = fields.Int()
    milestone_status = fields.Str()
    completed_date = fields.DateTime(),
    eval_date = fields.DateTime(),
    eval_score = fields.Float()
    eval_feedback = fields.Str()
    submission_id = fields.Int()


class MemberDetails(Schema):
    approval_status = fields.Str()
    discord_username =fields.Str()
    email = fields.Str()
    first_name = fields.Str()
    github_username = fields.Str()
    last_name = fields.Int()
    team_id = fields.Int()
    user_id = fields.Int()
    user_type = fields.Str()


class TeamDetails(Schema):
    team_id = fields.Int()
    project_id = fields.Int()
    team_lead_id = fields.Int()
    team_name = fields.Str()
    github_repo_url = fields.Str()
    members = fields.Nested(MemberDetails, many=True)
    milestone_statuses = fields.Nested(MilestoneStatusDetails, many=True)


class TADashboardTeamGetOutput(Schema):
    members = fields.Nested(MemberCommitsDetails, many=True)
    milestones = fields.Nested(MilestoneDetails, many=True)
    team = fields.Nested(TeamDetails)
