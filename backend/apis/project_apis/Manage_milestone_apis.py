from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Milestone
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.project_api.TADmilestone_api_outputs import (
    MilestoneCreationResponse,
    MilestoneUpdateResponse,
    MilestoneDeletionResponse,
    MilestoneListResponse
)
from datetime import datetime
from helpers.ErrorCommonHelpers import createFatalError
from flask import request
from api_parsers.milestone_definition_parser import MilestoneSchema, MilestoneUpdateSchema
from marshmallow import ValidationError

api_bp_milestones = Blueprint(
    "Manage Milestones APIs", "Manage Milestones", description="Operations for managing milestones"
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
            
            #Parse dates with proper validation
            try:
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
            except ValueError:
                return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
            
            new_milestone = Milestone(
                milestone_name=data["milestone_name"],
                milestone_description=data["milestone_description"],
                start_date=start_date,
                end_date=end_date,
                max_marks=data["max_marks"],
                project_id=data['project_id']
            )

            db.session.add(new_milestone)
            db.session.commit()

            return {
                "message": "Milestone created successfully"
            }, 201
        
        except ValidationError as e:
            return {"message": f"Validation error: {e.messages}"}, 400
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

            if "milestone_name" in data:
                milestone.milestone_name = data["milestone_name"]
            if "description" in data:
                milestone.milestone_description = data["milestone_description"]
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