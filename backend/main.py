from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User, Project, Milestone, MilestoneStatus, Member, Commit, Team, Submission, File
from config import Config, create_default_objects
import os
from utils.github_helpers import github_user_exists
from datetime import timedelta
from apis.team_apis.team_apis import api_bp_ta
from apis.stu_dashboard.stu_dashboard_apis import api_bp_stu
from apis.project_apis.Manage_milestone_apis import api_bp_milestones
from apis.project_apis.TADproject_apis import api_bp_projects
from apis.Ta_dashboard.submission_files import api_bp_submission
from apis.Ta_dashboard.commits_github import api_bp_GenAI
from apis.ta_teams_dashboard.ta_teams_dashboard import api_bp_ta_dashboard
from apis.user_apis.userAuthentication import api_bp_auth
from apis.taHomeAPIs.taHome_apis import api_bp_tahome


import logging
from flask_cors import CORS
from celery_config import make_celery
import tasks
from celery.result import AsyncResult


# from flask_restx import Api
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort

app = Flask(__name__)
# CORS(app)
# CORS(app)
app.config["API_TITLE"] = "Project Pulse API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["UPLOAD_FOLDER"] = "uploads"
api = Api(app)
app.config.from_object(Config)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)


celery = make_celery(app)


CORS(app)

#CORS(api)
# CORS(api)
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


CORS(api_bp_ta)
CORS(api_bp_projects)
CORS(api_bp_milestones)
CORS(api_bp_tahome)
CORS(api_bp_ta_dashboard)
CORS(api_bp_auth)
CORS(api_bp_stu)
CORS(api_bp_submission)
CORS(api_bp_GenAI)

api.register_blueprint(api_bp_ta)
api.register_blueprint(api_bp_projects)
api.register_blueprint(api_bp_milestones)
api.register_blueprint(api_bp_tahome)
api.register_blueprint(api_bp_ta_dashboard)
api.register_blueprint(api_bp_auth)
api.register_blueprint(api_bp_stu)
api.register_blueprint(api_bp_submission)
api.register_blueprint(api_bp_GenAI)


# api.add_namespace(api_bp_ta)
# api.add_namespace(api_bp_ta)


@app.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message": "It is working"}), 200


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, filename)

@app.route("/api/celery-test", methods=["POST"])
# @jwt_required()
# @check_access(roles=[MRoles.admin.value])
def download_theatre_csv():
    repo_url = request.json.get("repo_url")
    #current_user_id = get_jwt_identity()
    #print("request got for ",current_user_id,theatreId)
    #tasks.create_theatre_csv_celery.delay(theatreId,current_user_id)
    asyncTaskTheatre =  tasks.get_github_data.apply_async(args=[repo_url])
    print("returning from async task")
    return jsonify({
        "message": "File processing started. Do not close your browser as the file will be downloaded automatically.",
        "task_id": asyncTaskTheatre.id,
    })

@app.route("/api/task_status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    response = {
        "task_id": task_id,
        "status": task_result.status,
        #"result": task_result.result if task_result.ready() else None
    }
    return jsonify(response), 200



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database created successfully.")
            if not User.query.filter_by(email="admin@projectpulse.com").first():
                create_default_objects(db=db, app=app)
                logging.info("Default admin user created.")
            else:
                logging.info("Default admin user already exists.")
            if not User.query.filter_by(email="admin@projectpulse.com").first():
                create_default_objects(db=db, app=app)
                logging.info("Default admin user created.")
            else:
                logging.info("Default admin user already exists.")
        except Exception as e:
            logging.error(f"Error creating database: {e}")
    # Create default admin user if not exists
    with app.app_context():
        if not User.query.filter_by(email="admin@projectpulse.com").first():
            admin_user = User(
                first_name="Admin",
                last_name="ProjectPulse",
                password=bcrypt.generate_password_hash("projectpulse123").decode(
                    "utf-8"
                ),
                email="admin@projectpulse.com",
                github_username="pranjalkar99",
                discord_username="test123",
                user_type="Admin",
                approval_status="Active",
            )
            db.session.add(admin_user)
            db.session.commit()
            logging.info("Default admin user created.")
        else:
            logging.info("Default admin user already exists.")

    app.run(debug=True)
