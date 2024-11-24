from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from flask_smorest import Blueprint
from marshmallow import ValidationError
from models import User, Project, db
from api_outputs.project_api.TADmilestone_api_outputs import (
    ProjectCreationResponse,
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
    @jwt_required()
    @api_bp_projects.response(201, ProjectCreationResponse)
    def post(self):
        """ API to allow TAs and other allowed roles to create the project statement. """
        try:
            # Parse and validate incoming JSON data using the schema
            schema = CreateProjectSchema()
            data = schema.load(request.get_json())

            print('Received data:', data)

            # Get the current user ID from JWT
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return {"message": "Missing or invalid JWT token"}, 403
            
            current_user = User.query.get_or_404(current_user_id)

            # Check if the user has permission to create a project
            allowed_roles = ["TA", "Admin", "Instructor", "Developer"]
            if current_user.user_type not in allowed_roles:
                return {"message": "You do not have permission to create a project"}, 403

            # Create a new project
            new_project = Project(
                project_topic=data["name"],
                statement=data["statement"],
                document_url=data["document_url"],
            )
            db.session.add(new_project)
            db.session.commit()

            # Return response with the output schema
            return {
                "message": "Project created successfully",
                "project": {
                    "project_id": new_project.project_id,
                    "name": new_project.project_topic,
                    "statement": new_project.statement,
                    "document_url": new_project.document_url,
                },
            }, 201

        except KeyError as e:
            # Handle missing required fields
            return {"message": f"Missing required field: {str(e)}"}, 400

        except ValidationError as e:
            # Handle validation errors from Marshmallow
            return {"message": f"Validation error: {e.messages}"}, 400
        
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        except Exception as e:
            # Catch any other errors and return a generic error message
            return createFatalError(
                "project_creation_error",
                "Error creating the project",
                str(e),
            )
