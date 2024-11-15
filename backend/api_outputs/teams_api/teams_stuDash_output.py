from marshmallow import Schema, fields

class StuDashTeamSchema(Schema):
    team_name = fields.String(required=True, description="The name of the team")
    team_score = fields.Integer(required=True, description="The total score of the team based on evaluations")
    members = fields.List(fields.Nested(
        Schema.from_dict({
            'name': fields.String(required=True, description="The full name of the team member"),
            'email': fields.Email(required=True, description="Email address of the team member"),
            'commit_count': fields.Integer(required=True, description="The number of commits made by the member"),
        })
    ), required=True, description="List of team members with their names, emails, and commit counts")
