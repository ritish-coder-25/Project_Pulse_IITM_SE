from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Team, MilestoneStatus, Commit
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.api_outputs_common import TeamSchema, CommonErrorSchema, CommonErrorErrorSchemaFatal
from helpers.ErrorCommonHelpers import createError, createFatalError

# Blueprint for Student Dashboard API
api_bp_stu = Blueprint("StuDashboard-Api", "StuDashboard", description="Display of Student dashboard")

@api_bp_stu.route('/api/stu_home/<int:stu_id>')
class StuDashboard(Resource):
    @api_bp_stu.response(201, TeamSchema)
    @api_bp_stu.response(404, CommonErrorSchema)
    @jwt_required()
    def get(self, stu_id):
        try:
            current_user = User.query.get_or_404(stu_id)

            # Fetch the user's team if available
            if not current_user.team:
                return createError("team_get_curr_no_team", "User is not in a team", 404)
            
            team_data = {
                'team_name': current_user.team.team_name,
                'team_score': 0,
                'members': []
            }

            # Retrieve and add the team's score from milestones
            scores = MilestoneStatus.query.filter_by(team_id=current_user.team.team_id).all()
            team_data['team_score'] = sum(score.eval_score for score in scores)

            # Retrieve member data for the team, including commit counts
            for member in current_user.team.members:
                member_data = {
                    'name': f"{member.first_name} {member.last_name}",
                    'email': member.email,
                    'commit_count': Commit.query.filter_by(user_id=member.user_id).count()
                }
                team_data['members'].append(member_data)

        except Exception as e:
            db.session.rollback()
            return createFatalError("error", "An error occurred", str(e))
