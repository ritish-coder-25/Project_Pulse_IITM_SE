from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Milestone, Project
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.project_api.TADmilestone_api_outputs import (
    MilestoneCreationResponse,
    MilestoneUpdateResponse,
    MilestoneDeletionResponse,
    MilestoneListResponse,
    CommonErrorSchema,
    CommonErrorErrorSchemaFatal,
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
    @api_bp_milestones.arguments(MilestoneSchema)
    @api_bp_milestones.response(201, MilestoneCreationResponse)
    @api_bp_milestones.response(404, CommonErrorSchema)
    @jwt_required()
    def post(self, data):
        """Create a new milestone"""
        try:
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return {"message": "Missing or invalid JWT token"}, 403
            
            current_user = User.query.get_or_404(current_user_id)

            allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
            if current_user.user_type not in allowed_roles:
                return (jsonify(
                    {
                        "errorCode": "not_allowed_to_create_project_wrong_role",
                        "message": "You do not have permission to create a milestone"
                    }), 403,
                )
            
            #Parse dates with proper validation
            try:
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
            except ValueError:
                return (jsonify(
                    {
                        "errorCode": "invalid-date-format",
                        "message": "Invalid date format. Use YYYY-MM-DD"
                    }), 400,
                )
            
            #Select the first project from the database
            project = Project.query.first()
            if not project or project.project_id != 1:
                return(jsonify(
                    {
                        "errorCode": "no_projects_available",
                        "message": "No available projects found"
                    }), 404
                )
            
            new_milestone = Milestone(
                milestone_name=data["milestone_name"],
                milestone_description=data["milestone_description"],
                start_date=start_date,
                end_date=end_date,
                max_marks=data["max_marks"],
                project_id=1,
            )

            db.session.add(new_milestone)
            db.session.commit()

            return (jsonify(
                {
                    "message": "Milestone created successfully"
                }), 201
            )
        
        except Exception as e:
            db.session.rollback()
            return createFatalError(
                "milestone_creation_error",
                "Error occurred while creating milestone",
                str(e),
            )


    @jwt_required()
    @api_bp_milestones.response(200, MilestoneListResponse)
    @api_bp_milestones.response(404, CommonErrorSchema)
    def get(self):
        """Retrieve all milestones"""
        try:
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return {"message": "Missing or invalid JWT token"}, 403
            
            current_user = User.query.get_or_404(current_user_id)
            allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]

            if current_user.user_type not in allowed_roles:
                return (jsonify(
                    {
                        "errorCode": "not_allowed_to_fetch_milestones_wrong_role",
                        "message": "You do not have permission to read milestones"
                    }), 403
                )

            milestones = Milestone.query.all()
            milestones_data = [milestone.to_dict() for milestone in milestones]
            return (jsonify(milestones_data), 200)
        
        except Exception as e:
            return createFatalError(
                "milestone_fetch_error",
                "Error occurred while fetching milestones",
                str(e),
            )


@api_bp_milestones.route("/api/milestones/<int:milestone_id>")
class MilestoneResource(Resource):
    @jwt_required()
    @api_bp_milestones.arguments(MilestoneUpdateSchema)
    @api_bp_milestones.response(200, MilestoneUpdateResponse)
    @api_bp_milestones.response(404, CommonErrorSchema)
    def put(self, data, milestone_id):
        """Update an existing milestone"""
        try:
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return {"message": "Missing or invalid JWT token"}, 403
            
            current_user = User.query.get_or_404(current_user_id)
            allowed_roles = ["Admin", "TA", "Instructor", "Developer"]

            if current_user.user_type not in allowed_roles:
                return (jsonify(
                    {
                        "errorCode": "not_allowed_to_update_milestone_wrong_role",
                        "message": "You do not have permission to update milestone"
                    }), 403
                )

            #data = schema.load(request.get_json())  # Validate the incoming data

            milestone = Milestone.query.get_or_404(milestone_id)

            print(f"Received update data: {data}")
            print(f"Current milestone before update: {milestone}")

            if "milestone_name" in data:
                milestone.milestone_name = data["milestone_name"]
            if "milestone_description" in data:
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
            db.session.rollback()
            return createFatalError(
                "milestone_update_error",
                "Error occurred while updating milestone",
                str(e),
            )


    @jwt_required()
    @api_bp_milestones.response(200, MilestoneDeletionResponse)
    @api_bp_milestones.response(404, CommonErrorSchema)
    def delete(self, milestone_id):
        """Delete a milestone"""
        try:
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return {"message": "Missing or invalid JWT token"}, 403
            
            current_user = User.query.get_or_404(current_user_id)
            allowed_roles = ["Admin", "TA", "Instructor", "Developer"]

            if current_user.user_type not in allowed_roles:
                return (jsonify({"message": "You do not have permission to delete milestones"}), 403)

            milestone = Milestone.query.get_or_404(milestone_id)
            db.session.delete(milestone)
            db.session.commit()
            return (jsonify({"message": "Milestone deleted successfully"}), 200)
        
        except Exception as e:
            db.session.rollback()
            return createFatalError(
                "milestone_deletion_error",
                "Error occurred while deleting milestone",
                str(e),
            )