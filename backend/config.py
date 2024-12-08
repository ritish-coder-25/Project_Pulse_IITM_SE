from datetime import timedelta, datetime
import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import *

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "test123")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "test123")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


def create_default_objects(db, app):
    bcrypt = Bcrypt(app)
    # Create a default project
    default_project = Project(
        project_topic="PROJECT DETAILS  SEP’24",
        statement="Tracking Student Progress in Software Projects",
        document_url="https://docs.google.com/document/d/1n7AxCUoBJuDVxIVGGz_jh72hGY4ICQ2tg0tAvJHHMqU/edit?tab=t.0#heading=h.uqcmipq6429b",
    )
    db.session.add(default_project)
    db.session.flush()  # To get the project_id for foreign keys

    # Create a default team
    default_team = Team(
        team_name="Sample Team",
        github_repo_url="https://github.com/sample_repo",
        project_id=default_project.project_id,
    )
    db.session.add(default_team)
    db.session.flush()  # To get the team_id for foreign keys

    # Create a default user
    default_user = User(
        first_name="Admin",
        last_name="ProjectPulse",
        password=bcrypt.generate_password_hash("projectpulse123").decode("utf-8"),
        email="admin@projectpulse.com",
        github_username="pranjalkar99",
        discord_username="test123",
        user_type="Admin",
        approval_status="Active",
    )
    db.session.add(default_user)
    db.session.flush()  # To get the user_id for foreign keys

    # Create a default milestone
    default_milestone = Milestone(
        milestone_name="Sample Milestone",
        milestone_description="This is a sample milestone description.",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        max_marks=100,
        project_id=default_project.project_id,
    )
    db.session.add(default_milestone)
    db.session.flush()  # To get the milestone_id for foreign keys

    # Create a default submission
    default_submission = Submission(
        team_id=default_team.team_id, milestone_id=default_milestone.milestone_id
    )
    db.session.add(default_submission)
    db.session.flush()  # To get the submission_id for foreign keys

    # Create a default file
    default_file = File(
        file_name="sample_file.txt", submission_id=default_submission.submission_id
    )
    db.session.add(default_file)

    # Create a default milestone status
    default_milestone_status = MilestoneStatus(
        team_id=default_team.team_id,
        milestone_id=default_milestone.milestone_id,
        milestone_status="Pending",
        eval_date=None,
        completed_date=None,
        eval_score=None,
        eval_feedback=None,
        submission_id=default_submission.submission_id,
    )
    db.session.add(default_milestone_status)

    # Create a default commit
    default_commit = Commit(
        user_id=default_user.user_id,
        team_id=default_team.team_id,
        commit_hash="abcdef123456",
        commit_message="Initial commit",
        commit_score=10.0,
        commit_url="https://github.com/sample_repo/commit/abcdef123456",
    )
    db.session.add(default_commit)

    # Commit the transaction
    db.session.commit()
