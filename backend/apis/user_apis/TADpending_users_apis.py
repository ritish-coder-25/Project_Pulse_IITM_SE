from flask import request, jsonify
from flask_jwt_extended import jwt_required
from models import User
from flask_jwt_extended import get_jwt_identity
from backend.api_parsers import TADpending_user_parsers
from flask_restx import Resource
from flask_smorest import Blueprint
from backend.api_outputs.user_api.TADpending_user_outputs import PendingUserListOutput
from helpers.ErrorCommonHelpers import createError, createFatalError
from helpers.ErrorCommonHelpers import createError, createFatalError

api_bp_pu = Blueprint(
    "PendingUsers-Api", "PendingUsers", description="Operations to get pending users"
)


@api_bp_pu.route("/api/pendusers")
class PendingUserListResource(Resource):
    @jwt_required()
    @api_bp_pu.response(200, PendingUserListOutput)
    def get(self):
        try:
            # Query for pending users
            pending_users = User.query.filter_by(approval_status="Inactive").all()
            result = [
                {
                    "id": user.user_id,
                    "name": f"{user.first_name} {user.last_name}",
                    "email": user.email,
                }
                for user in pending_users
            ]
            return (
                jsonify(
                    {
                        "pending_users": result,
                    }
                ),
                200,
            )
        except Exception as e:
            # Use a standardized error response
            return createFatalError(
                "pending_users_fetch_error", "Error fetching pending users", str(e)
            )
