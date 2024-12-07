from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from flask_restx import Resource
from flask_smorest import Blueprint
from helpers.ErrorCommonHelpers import createError, createFatalError
from utils.github_helpers import github_user_exists
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta
from flask_bcrypt import Bcrypt
from api_outputs.user_api.TADpending_user_outputs import PendingUserOutput
from api_outputs.user_api.TADuser_approval_outputs import UserApprovalOutput
from api_parsers.TADuser_approval_parsers import ApproveUsersRequest

api_bp_auth = Blueprint(
    "User Mantainence APIs",
    "User Mantainence APIs",
    description="Operations for User Registration, Approval and Login",
)

bcrypt = Bcrypt()
@api_bp_auth.route("/api/auth/register", methods=["POST"])
class RegisterResource(Resource):
    # @jwt_required()

    def post(self):
        """API for new user registration"""
        data = request.get_json()
        bcrypt = Bcrypt()
        required_fields = [
            "first_name",
            "last_name",
            "password",
            "email",
            "github_username",
            "discord_username",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing {field}"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email already registered"}), 400

        if User.query.filter_by(github_username=data["github_username"]).first():
            return jsonify({"message": "GitHub username already registered"}), 400

        if User.query.filter_by(discord_username=data["discord_username"]).first():
            return jsonify({"message": "Discord username already registered"}), 400

        if len(data["password"]) < 8:
            return (
                jsonify({"message": "Password must be at least 8 characters long"}),
                400,
            )

        if not github_user_exists(data["github_username"]):
            return jsonify({"message": "GitHub username does not exist"}), 400

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
            "utf-8"
        )

        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=hashed_password,
            email=data["email"],
            github_username=data["github_username"],
            discord_username=data["discord_username"],
            user_type="Registered",
            approval_status="Inactive",
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify({"isSuccess": True, "message": "User registered successfully"}),
            201,
        )


@api_bp_auth.route("/api/auth/login", methods=["POST"])
class LoginResource(Resource):
    def post(self):
        """API for user login"""
        try: 
            data = request.get_json()
            user = User.query.filter_by(email=data["email"]).first()

            if user and bcrypt.check_password_hash(user.password, data["password"]):
                expires = timedelta(days=90)
                access_token = create_access_token(
                    identity=user.user_id, expires_delta=expires
                )
                jsonified = jsonify({"access_token": access_token, "user": user.to_dict()})
                return jsonified, 200

            return jsonify({"errorCode": "invalid_login","message": "Invalid credentials"}), 401
        except Exception as e:
            return createFatalError(
                "user_login_error",
                "Error login in user",
                str(e),
            )

@api_bp_auth.route("/api/users/pendusers")
class PendingUserListResource(Resource):
    @jwt_required()
    @api_bp_auth.response(200, PendingUserOutput)
    def get(self):
        """API to get the pending users awaiting authorization for registration."""
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


@api_bp_auth.route("/api/users/approve_users")
class ApproveUsersResource(Resource):
    @jwt_required()
    @api_bp_auth.arguments(ApproveUsersRequest)
    @api_bp_auth.response(200, UserApprovalOutput)
    def post(self, data):
        """API for TA to approve the new user registrations (app only)"""
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
                user_id = user_data.get("user_id")
                approval_status = user_data.get("approval_status")
                user_type = user_data.get("user_type")

                user = User.query.get(user_id)
                if not user:
                    results.append({"user_id": user_id, "message": "User not found"})
                    continue
                user.user_type = user_type
                if approval_status == "Approved":
                    user.approval_status = "Active"
                elif approval_status == "Declined":
                    user.approval_status = "Decline"
                else:
                    results.append(
                        {"user_id": user_id, "message": "Invalid approval_status"}
                    )
                    continue

                db.session.commit()
                results.append(
                    {"user_id": user_id, "message": "User approval processed"}
                )

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
        
@api_bp_auth.route('/api/users', methods=['GET'])
class UserResource(Resource):
    @jwt_required()
    def get(self):
        query_params = request.args  # Get all query parameters from the URL

        # If 'id' is present, fetch the exact user by id
        user_id = query_params.get('id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify(user.to_dict()), 200
            else:
                return jsonify({"error": "User not found"}), 404


        query = User.query


        for field, value in query_params.items():
            if field != 'id' and hasattr(User, field):

                column_type = str(getattr(User, field).type)
                print(column_type)
                if 'VARCHAR' in column_type:
                    query = query.filter(getattr(User, field).like(f'%{value}%'))
                else:

                    query = query.filter(getattr(User, field) == value)


        users = query.all()
        jsonUsers = jsonify([user.to_dict() for user in users])
        return jsonUsers, 200
