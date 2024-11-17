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
from flask_bcrypt import bcrypt

api_bp_auth = Blueprint(
    "UserAuthentication-Api",
    "UserAuthentication",
    description="Operations for User Registration and Login",
)


@api_bp_auth.route("/api/auth/register", methods=["POST"])
class RegisterResource(Resource):
    # @jwt_required()

    def post(self):
        """API for user registration"""
        data = request.get_json()

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
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()

        if user and bcrypt.check_password_hash(user.password, data["password"]):
            expires = timedelta(days=90)
            access_token = create_access_token(
                identity=user.user_id, expires_delta=expires
            )
            jsonified = jsonify({"access_token": access_token, "user": user.to_dict()})
            return jsonified, 200

        return jsonify({"message": "Invalid credentials"}), 401
