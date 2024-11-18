from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import MilestoneStatus
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.project_api.TADmilestone_api_outputs import MilestoneCompletionsResponse
from datetime import datetime, timedelta, timezone
from helpers.ErrorCommonHelpers import createFatalError

api_bp_milestone_completions = Blueprint(
    "MilestoneCompletions-Api",
    "MilestoneCompletions",
    description="Operation for getting milestone completions in last 7 days",
)



@api_bp_milestone_completions.route("/api/project/milecomps")
class MilestoneCompletionsResource(Resource):
    @jwt_required()
    @api_bp_milestone_completions.response(200, MilestoneCompletionsResponse)
    def get(self):
        try:
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

            recent_milestone_completions = MilestoneStatus.query.filter(
                MilestoneStatus.completed_date >= seven_days_ago,
                MilestoneStatus.milestone_status == "Completed",
            ).all()

            result = [
                {"team": milestone.team.team_name}
                for milestone in recent_milestone_completions
                if milestone.team
            ]

            if not result:
                return (
                    jsonify(
                        {
                            "message": "No milestone completions in the last 7 days",
                        }
                    ),
                    200,
                )

            return jsonify({"completions": result}), 200
        except Exception as e:
            return createFatalError(
                "milecomps_fetching_error",
                "Error fetching milestone completions",
                str(e),
            )

