from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from flask_smorest import Blueprint
from marshmallow import ValidationError
from models import User, Project, db
from api_outputs.project_api.TADmilestone_api_outputs import (
    ProjectCreationResponse,
    CommonErrorSchema,
    CommonErrorErrorSchemaFatal,
)
from api_parsers.project_definition_parser import CreateProjectSchema
from helpers.ErrorCommonHelpers import createFatalError
import jwt


api_bp_projects = Blueprint(
    "Manage Projects APIs",
    "Manage Projects",
    description="Operations related to creating and managing projects",
)


@api_bp_projects.route("/api/projects")
class CreateProjectResource(Resource):
    @api_bp_projects.arguments(CreateProjectSchema)
    @api_bp_projects.response(404, CommonErrorSchema)
    @api_bp_projects.response(201, ProjectCreationResponse)
    @jwt_required()
    def post(self, data):
        """ API to allow TAs and other allowed roles to create the project statement. """
        try:
            # Parse and validate incoming JSON data using the schema
            #schema = CreateProjectSchema()
            #data = schema.load(request.get_json())

            print('Received data:', data)

            # Get the current user ID from JWT
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return {"message": "Missing or invalid JWT token"}, 403
            
            current_user = User.query.get_or_404(current_user_id)

            # Check if the user has permission to create a project
            allowed_roles = ["TA", "Admin", "Instructor", "Developer"]
            if current_user.user_type not in allowed_roles:
                return (
                    jsonify(
                        {
                            "errorCode": "not_allowed_to_create_project_wrong_role",
                            "message": "You do not have permission to create a project",
                        }
                    ), 403,
                )

            project_id = 1  
            project = Project.query.get(project_id)

            if project:
                # Update the project's attributes with the new details
                project.project_topic = data["name"]
                project.statement = data["statement"]
                project.document_url = data["document_url"]
                db.session.commit()
            else:
                print(f"Project with ID {project_id} does not exist.")
            # Return response with the output schema
            return (jsonify({
                "message": "Project created successfully",
                "project": {
                    "project_id": project.project_id,
                    "name": project.project_topic,
                    "statement": project.statement,
                    "document_url": project.document_url,
                },
            }), 201)


        except KeyError as e:
            # Handle missing required fields
            return (
                jsonify(
                    {
                        "errorCode": "missing_required_field",
                        "message": f"Missing required field: {str(e)}",
                    }
                ), 400,
            )

        # except ValidationError as e:
        #     # Handle validation errors from Marshmallow
        #     return (
        #         jsonify(
        #             {
        #                 "errorCode": "validation_error",
        #                 "message": f"Validation error: {e.messages}",
        #             }
        #         ), 400,
        #     )
        
        except jwt.ExpiredSignatureError:
            return (
                jsonify(
                    {
                        "errorCode": "expired_token",
                        "message": "Token has expired",
                    }
                ), 401,
            )
        except jwt.InvalidTokenError:
            return (
                jsonify(
                    {
                        "errorCode": "invalid_token",
                        "message": "Invalid token",
                    }
                ), 401,
            )

        except Exception as e:
            db.session.rollback()
            # Catch any other errors and return a generic error message
            return createFatalError(
                "project_creation_error",
                "Error creating the project",
                str(e),
            )

@api_bp_projects.route('/api/projects')
class SubmitProject(Resource):
    @api_bp_projects.response(201, CreateProjectSchema)
    @api_bp_projects.response(400, CommonErrorSchema)
    # @jwt_required()
    def get(self):
        """Retrieve details for Project 1 in the database."""
        try:
            proj_details = Project.query.filter_by(project_id=1).first()
            if not proj_details:
                return {
                    "error": "proj_fetch_error",
                    "message": "No project with project ID = 1 exists in the system"
                }, 400

            result = {
                "name": proj_details.project_topic,
                "statement": proj_details.statement,
                "document_url": proj_details.document_url,
            }
            return jsonify(result), 200

        except Exception as e:
            return {
                "error": "proj_fetch_error",
                "message": "An unexpected error occurred while fetching the project",
                "details": str(e),
            }, 500

