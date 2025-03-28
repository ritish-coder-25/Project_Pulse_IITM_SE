from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint 
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from models import (
    User,
    Team,
    Milestone,
    MilestoneStatus,
    Commit
)
from flask_jwt_extended import get_jwt_identity
from api_outputs.ta_dashboard_api.ta_dashboard_api_output import TADashboardTeamsGetOutput, TADashboardTeamGetOutput
from helpers.ErrorCommonHelpers import createError, createFatalError
from api_outputs.api_outputs_common import CommonErrorSchema, CommonErrorErrorSchemaFatal
from constants import TA_ALLOWED_ROLES, ACTIVE
import traceback

api_bp_ta_dashboard = Blueprint("Fetch TADashboard APIs", "Fetch TADashboard", description="Operations to fetch TA Dashboard")


@api_bp_ta_dashboard.route("/api/ta-teams")
class TATeamDashboard(MethodView):
    
    @jwt_required()
    @api_bp_ta_dashboard.response(200, TADashboardTeamsGetOutput)
    @api_bp_ta_dashboard.response(403, CommonErrorSchema)
    @api_bp_ta_dashboard.response(500, CommonErrorSchema)
    def get(self):
        """
        API to get data for rendering Teams Dashboard for TA
        """
        
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)

        allowed_roles = TA_ALLOWED_ROLES
        if current_user.user_type not in allowed_roles:
            return createError("user_does_not_have_permission_to_access_dashboard", "User does not have permission to access dashboard", 403)
        
        if current_user.approval_status != 'Active':
            return createError("user_does_not_have_permission_to_access_dashboard", "User does not have permission to access dashboard", 403)
           
        try:
            teams = Team.query.all()

            commit_counts = Commit.query.with_entities(Commit.team_id, func.count(Commit.commit_id)).group_by(Commit.team_id).all()
            # output format for above query is [ ("team_id", "commit_count"), ("team_id", "commit_count") , ... ]
            commit_counts = {i[0]: i[1] for i in commit_counts}
            
            milestones = Milestone.query.all()
            milestone_data = { milestone.milestone_id: milestone for milestone in milestones }

            milestone_statuses = MilestoneStatus.query.all()

            dashboard_teams = {}

            for team in teams:
                comm_counts = commit_counts.get(team.team_id, 0)
                dashboard_teams[team.team_id] = { "team_id": team.team_id, "team_name": team.team_name, "commits": comm_counts,
                            "score": 0, "total_score": 0, "milestones_completed": 0, "milestones_missed": 0 }

            for status in milestone_statuses:

                if status.milestone_status == "Evaluated":
                    dashboard_teams[status.team_id]['score'] += status.eval_score
                    if milestone_data and status.milestone_id and milestone_data.get(status.milestone_id):
                        dashboard_teams[status.team_id]['total_score'] += milestone_data[status.milestone_id].max_marks
                    dashboard_teams[status.team_id]['milestones_completed'] += 1
                elif status.milestone_status == "Missed":
                    dashboard_teams[status.team_id]['score'] += 0
                    dashboard_teams[status.team_id]['total_score'] += milestone_data[status.milestone_id].max_marks
                    dashboard_teams[status.team_id]['milestones_missed'] += 1

            return jsonify({"teams": [dashboard_teams[team] for team in dashboard_teams], "milestones": [milestone.to_dict() for milestone in milestones]})
        
        except Exception as e:
            print(traceback.format_exc())
            return createError("ta_dashbaord_teams_server_error", "Error while fetching dashboard data", 500)




@api_bp_ta_dashboard.route("/api/ta-teams/<int:team_id>")
class TATeamDashboard(MethodView):

    @jwt_required()
    @api_bp_ta_dashboard.response(200, TADashboardTeamGetOutput)
    @api_bp_ta_dashboard.response(403, CommonErrorSchema)
    @api_bp_ta_dashboard.response(500, CommonErrorSchema)
    def get(self, team_id):
        """
        API to get data for rendering Individual Team's Dashboard for TA
        """
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get_or_404(current_user_id)

            allowed_roles = TA_ALLOWED_ROLES
            if current_user.user_type not in allowed_roles:
                return createError("user_does_not_have_permission_to_access_dashboard", "User does not have permission to access dashboard", 403)

            if current_user.approval_status != 'Active':
                return createError("user_does_not_have_permission_to_access_dashboard", "User does not have permission to access dashboard", 403)

            team = Team.query.get_or_404(team_id)

        
            commit_counts = Commit.query.filter(Commit.team_id==team_id).with_entities(Commit.user_id, func.count(Commit.commit_id)).group_by(Commit.user_id).all()
            # output format for above query is [ ("user_id", "commit_count"), ("user_id", "commit_count") , ... ]
            commit_counts = {i[0]: i[1] for i in commit_counts}

            members = User.query.filter(User.team_id==team.team_id).all()
            members_data = {member.user_id: {"name": f"{member.first_name} {member.last_name}", "email": member.email, "commits": commit_counts.get(member.user_id, 0)} for member in members }

            milestones = Milestone.query.all()

            return jsonify({"members": [members_data[member] for member in members_data], 
                            "team": team.to_dict(), 
                            "milestones": [milestone.to_dict() for milestone in milestones]
                            })
        
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            return {
                "errorCode": "unknown_error",
                "message": "An unexpected error occurred.",
                "error": str(e),
          }, 500

 