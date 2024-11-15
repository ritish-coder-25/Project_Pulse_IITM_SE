from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from config import Config
from routes import api_bp, api_bp_users
from ta_routes import api_ta
from apis.team_apis.team_apis import api_bp_ta
from utils.github_helpers import github_user_exists
from datetime import timedelta
import logging
from flask_cors import CORS
#from flask_restx import Api
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort

app = Flask(__name__)
#CORS(app)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
api = Api(app)
CORS(app)
app.config.from_object(Config)

#CORS(api)
# Enable CORS for all routes

# api = Api(
#     app,
#     version="1.0",
#     title="API Documentation",
#     description="A description of your API",
# )


db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


api.register_blueprint(api_bp_ta)
api.register_blueprint(api_bp_users)

app.register_blueprint(api_bp)
app.register_blueprint(api_ta)

api.register_blueprint(api_bp_stu)

#api.add_namespace(api_bp_ta)


@app.route("/api/auth/register", methods=["POST"])
def register():
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
        return jsonify({"message": "Password must be at least 8 characters long"}), 400

    if not github_user_exists(data["github_username"]):
        return jsonify({"message": "GitHub username does not exist"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

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

    return jsonify({"isSuccess": True, "message": "User registered successfully"}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        expires = timedelta(days=90)
        access_token = create_access_token(identity=user.user_id, expires_delta=expires)
        jsonified = jsonify({"access_token": access_token, "user": user.to_dict()})
        return jsonified, 200

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message": "It is working"}), 200


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database created successfully.")
        except Exception as e:
            logging.error(f"Error creating database: {e}")
    app.run(debug=True)

    # Create default admin user if not exists
    with app.app_context():
        if not User.query.filter_by(student_email='admin@projectpulse.com').first():
            admin_user = User(
                first_name='Admin',
                last_name='ProjectPulse',
                password=bcrypt.generate_password_hash('projectpulse123').decode('utf-8'),
                student_email='admin@projectpulse.com',
                github_username='pranjalkar99',
                discord_username='test123',
                user_type='Admin',
                status='Active',
            )
            db.session.add(admin_user)
            db.session.add(main_project)
            db.session.commit()
            logging.info("Default admin user created.")
        else:
            logging.info("Default admin user already exists.")
