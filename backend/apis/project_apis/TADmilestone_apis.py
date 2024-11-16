from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import MilestoneStatus, User, Project, Milestone
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.project_api.TADmilestone_api_outputs import (
    MilestoneCompletionsResponse,
    MilestoneCreationResponse,
    MilestoneUpdateResponse,
    MilestoneDeletionResponse,
    MilestoneListResponse
)
from datetime import datetime, timedelta, timezone
from helpers.ErrorCommonHelpers import createFatalError

from api_parsers.milestone_definition_parser import MilestoneSchema, MilestoneUpdateSchema

api_bp_milestone_completions = Blueprint(
    "MilestoneCompletions-Api",
    "MilestoneCompletions",
    description="Operation for getting milestone completions in last 7 days",
)

api_bp_milestones = Blueprint(
    "Milestones-Api", "Milestones", description="Operations for managing milestones"
)


@api_bp_milestone_completions.route("/api/milecomps")
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
                            "completions": [],
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


@api_bp_milestones.route("/api/milestones")
class MilestonesResource(Resource):
    @jwt_required()
    @api_bp_milestones.response(201, MilestoneCreationResponse)
    def post(self):
        """Create a new milestone"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get_or_404(current_user_id)

            allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
            if current_user.user_type not in allowed_roles:
                return {"message": "You do not have permission to create a milestone"}, 403

            schema = MilestoneSchema()
            data = schema.load(request.get_json())  # Validate the incoming data

            new_milestone = Milestone(
                name=data["name"],
                description=data["description"],
                start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
                end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
                max_marks=data["max_marks"],
            )

            db.session.add(new_milestone)
            db.session.commit()

            return {
                "message": "Milestone created successfully",
                "milestone_id": new_milestone.id,
            }, 201
        except Exception as e:
            return createFatalError(
                "milestone_creation_error",
                "Error occurred while creating milestone",
                str(e),
            )


    @jwt_required()
    @api_bp_milestones.response(200, MilestoneListResponse)
    def get(self):
        """Retrieve all milestones"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get_or_404(current_user_id)

            allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
            if current_user.user_type not in allowed_roles:
                return {"message": "You do not have permission to read milestones"}, 403

            milestones = Milestone.query.all()
            return {"milestones": [milestone.to_dict() for milestone in milestones]}, 200
        except Exception as e:
            return createFatalError(
                "milestone_fetch_error",
                "Error occurred while fetching milestones",
                str(e),
            )


@api_bp_milestones.route("/api/milestones/<int:milestone_id>")
class MilestoneResource(Resource):
    @jwt_required()
    @api_bp_milestones.response(200, MilestoneUpdateResponse)
    def put(self, milestone_id):
        """Update an existing milestone"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get_or_404(current_user_id)

            allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
            if current_user.user_type not in allowed_roles:
                return {"message": "You do not have permission to update milestone"}, 403

            schema = MilestoneUpdateSchema()
            data = schema.load(request.get_json())  # Validate the incoming data

            milestone = Milestone.query.get_or_404(milestone_id)

            if "name" in data:
                milestone.name = data["name"]
            if "description" in data:
                milestone.description = data["description"]
            if "start_date" in data:
                milestone.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
            if "end_date" in data:
                milestone.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
            if "max_marks" in data:
                milestone.max_marks = data["max_marks"]

            db.session.commit()
            return {"message": "Milestone updated successfully"}, 200
        except Exception as e:
            return createFatalError(
                "milestone_update_error",
                "Error occurred while updating milestone",
                str(e),
            )


    @jwt_required()
    @api_bp_milestones.response(200, MilestoneDeletionResponse)
    def delete(self, milestone_id):
        """Delete a milestone"""
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get_or_404(current_user_id)

            allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
            if current_user.user_type not in allowed_roles:
                return {"message": "You do not have permission to delete milestones"}, 403

            milestone = Milestone.query.get_or_404(milestone_id)
            db.session.delete(milestone)
            db.session.commit()
            return {"message": "Milestone deleted successfully"}, 200
        except Exception as e:
            return createFatalError(
                "milestone_deletion_error",
                "Error occurred while deleting milestone",
                str(e),
            )