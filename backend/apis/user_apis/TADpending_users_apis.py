from flask import request, jsonify
from flask_jwt_extended import jwt_required
from models import User
from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.user_api.TADpending_user_outputs import PendingUserListOutput
from helpers.ErrorCommonHelpers import createError, createFatalError
from marshmallow import Schema, fields

api_bp_pu = Blueprint(
    "PendingUsers-Api", "PendingUsers", description="Operations to get pending users"
)


@api_bp_pu.route("/api/users/pendusers")
class PendingUserListResource(Resource):
    @jwt_required()
    @api_bp_pu.response(200, PendingUserListOutput)
    def get(self):
        try:
            pending_users = User.query.filter_by(approval_status="Inactive").all()
            result = [
                {
                    "id": user.user_id,
                    "name": f"{user.first_name} {user.last_name}",
                    "email": user.email,
                    "role": user.user_type if user.user_type else "Student",
                }
                for user in pending_users
            ]
            return jsonify(result)

        except Exception as e:
            return createFatalError(
                "pending_users_fetch_error", "Error fetching pending users", str(e)
            )
