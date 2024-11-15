# apis/user_apis/user_approval_api.py

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from flask_restx import Resource
from flask_smorest import Blueprint
from backend.api_outputs.user_api.TADuser_approval_outputs import UserApprovalOutput
from backend.api_parsers.TADuser_approval_parsers import ApproveUsersRequest
from helpers.ErrorCommonHelpers import createError, createFatalError

api_bp_ua = Blueprint(
    "UserApproval-Api", "UserApproval", description="Operations for approving users"
)


@api_bp_ua.route("/api/approve_users")
class ApproveUsersResource(Resource):
    @jwt_required()
    @api_bp_ua.arguments(ApproveUsersRequest)
    @api_bp_ua.response(200, UserApprovalOutput)
    def post(self, data):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get_or_404(current_user_id)
            allowed_roles = ["TA", "Admin", "Instructor", "Developer"]

            if current_user.user_type not in allowed_roles:
                return createError(
                    "approve_users_permission_denied",
                    "You do not have permission to approve users",
                    403,
                )

            results = []
            for user_data in data["users"]:
                user_id = user_data["id"]
                approved = user_data.get("approved")
                rejected = user_data.get("rejected")
                role = user_data.get("role", "Student")

                user = User.query.get(user_id)
                if not user:
                    results.append({"id": user_id, "message": "User not found"})
                    continue

                if approved:
                    user.approval_status = "Active"
                elif rejected:
                    user.approval_status = "Decline"

                # Update the user's role
                user.user_type = role
                db.session.commit()

                results.append({"id": user_id, "message": "User approval processed"})

            return (
                jsonify(
                    {
                        "message": "User approvals processed successfully",
                        "results": results,
                    }
                ),
                200,
            )
        except Exception as e:
            return createFatalError(
                "user_approval_processing_error",
                "Error processing user approvals",
                str(e),
            )
