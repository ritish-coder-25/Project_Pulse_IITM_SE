from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Team, MilestoneStatus, Commit, Milestone
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.api_outputs_common import CommonErrorSchema, CommonErrorErrorSchemaFatal
from api_outputs.teams_api.teams_stuDash_output import StuDashTeamSchema
from helpers.ErrorCommonHelpers import createError, createFatalError

# Blueprint for Student Dashboard API
api_bp_stu = Blueprint("StuDashboard-Api", "StuDashboard", description="Display of Student dashboard")

@api_bp_stu.route('/api/stu_home/<int:stu_id>')
class StuDashboard(Resource):
    @api_bp_stu.response(201, StuDashTeamSchema)
    @api_bp_stu.response(404, CommonErrorSchema)
    @jwt_required()
    def get(self, stu_id):
        """This API endpoint is to retrieve information about a student's team, providing an overview of the student's team activities and progress."""
        try:
            current_user = User.query.get_or_404(stu_id)
            if not current_user.team_id:
                return createError("team_get_curr_no_team", "User is not in a team", 404)
            team = Team.query.get_or_404(current_user.team_id)
                        
            team_data = {
                'team_name': team.team_name,
                'team_score': 0,
                'members': [], 
                'milestones': []
            }
            # Retrieve and add the team's score from milestones
            statuses = MilestoneStatus.query.filter_by(team_id=team.team_id).all()
            team_data['team_score'] = sum(status.eval_score or 0 for status in statuses)
            
            # Retrieve member data for the team, including commit counts
            for member in team.members:
                member_data = {
                    'name': f"{member.first_name} {member.last_name}",
                    'email': member.email,
                    'commit_count': Commit.query.filter_by(user_id=member.user_id).count()
                }
                team_data['members'].append(member_data)
                
            # Fetch milestone details
            for status in statuses:
                milestone = Milestone.query.get(status.milestone_id)
                if milestone:
                    milestone_data = {
                        'milestone_name': milestone.milestone_name,
                        'milestone_status': status.milestone_status,
                        'end_date': milestone.end_date
                    }
                    team_data['milestones'].append(milestone_data)

            return jsonify(team_data), 200

        except Exception as e:
            db.session.rollback()
            return createFatalError("error", "An error occurred", str(e))