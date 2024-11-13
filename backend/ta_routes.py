from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import (
    db,
    User,
    Team,
    Project,
    Milestone,
    MilestoneStatus,
    Commit,
    Submission,
)
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import get_jwt_identity

api_ta = Blueprint("api_ta", __name__)


# (Parag) TAHomePage - Fetching pending Users for approval
@api_ta.route("/api/pendusers", methods=["GET"])
# @jwt_required()
def get_pending_users():
    try:
        pending_users = User.query.filter_by(status="Inactive").all()
        result = [
            {
                "id": user.id,
                "name": f"{user.first_name} {user.last_name}",
                "email": user.student_email,
            }
            for user in pending_users
        ]
        return jsonify(result), 200
    except Exception as e:
        return (
            jsonify({"message": "Error fetching pending users", "error": str(e)}),
            500,
        )


# (Parag) TAHomePage - Returning approve/reject for users
@api_ta.route("/api/approve_users", methods=["POST"])
# @jwt_required()
def approve_usersTA():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    allowed_roles = ["TA", "Admin", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return jsonify({"message": "You do not have permission to approve users"}), 403
    users = data.get("users", [])
    for user_data in users:
        user_id = user_data.get("id")
        approved = user_data.get("approved")
        rejected = user_data.get("rejected")
        role = user_data.get("role", "Student")  # Default role as 'Student'
        user = User.query.get(user_id)
        if not user:
            continue  # Skip if user not found
        # Update user status based on approval or rejection
        if approved:
            user.status = "Active"
        elif rejected:
            user.status = "Decline"
        # Update the user's role
        user.role = role
        db.session.commit()

    return jsonify({"message": "User approvals processed successfully"}), 200


# (Parag) TAHomePage - Fetching uploads for last 7 days
@api_ta.route("/api/uploads", methods=["GET"])
# @jwt_required()
def get_uploads():
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_submissions = (
            db.session.query(Submission)
            .join(Team, Submission.team_id == Team.id)
            .filter(Submission.submission_timestamp >= seven_days_ago)
            .all()
        )
        result = [{"team": submission.team.name} for submission in recent_submissions]
        if not result:
            return jsonify({"message": "No uploads in the last 7 days"}), 200
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error fetching uploads", "error": str(e)}), 500


# (Parag) TAHomePage - Fetching commits for last 7 days
@api_ta.route("/api/commits", methods=["GET"])
# @jwt_required()
def get_commits():
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_commits = Commit.query.filter(Commit.timestamp >= seven_days_ago).all()
        result = [
            {"team": commit.user.team.name}
            for commit in recent_commits
            if commit.user and commit.user.team
        ]
        if not result:
            return jsonify({"message": "No commits in the last 7 days"}), 200
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error fetching commits", "error": str(e)}), 500


# (Parag) TAHomePage - Fetching milestone completions for last 7 days
@api_ta.route("/api/milecomps", methods=["GET"])
# @jwt_required()
def get_milecomps():
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_milestone_completions = MilestoneStatus.query.filter(
            MilestoneStatus.completed_date >= seven_days_ago,
            MilestoneStatus.status == "Completed",
        ).all()
        result = [
            {"team": milestone.team.name}
            for milestone in recent_milestone_completions
            if milestone.team
        ]
        if not result:
            return (
                jsonify({"message": "No milestone completions in the last 7 days"}),
                200,
            )
        return jsonify(result), 200
    except Exception as e:
        return (
            jsonify(
                {"message": "Error fetching milestone completions", "error": str(e)}
            ),
            500,
        )


##########################


@api_ta.route("/api/users_allocate", methods=["POST"])
@jwt_required()
def allocate_users():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return jsonify({"message": "You do not have permission to approve users"}), 403

    team_id = data["team_id"]
    users = data["users"]

    for user_id in users:
        user = User.query.get(user_id)
        user.team_id = team_id
        db.session.commit()

    return jsonify({"message": "Users allocated to team successfully"}), 200


@api_ta.route("/api/users_approval", methods=["POST"])
@jwt_required()
def users_approval():

    data = request.get_json()

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return jsonify({"message": "You do not have permission to approve users"}), 403

    status = data["status"]
    role = data["role"]

    if status not in ["Active", "Inactive", "Decline"]:
        return jsonify({"message": "Invalid status"}), 400
    if role not in ["Student", "TA", "Admin", "Instructor", "Developer"]:
        return jsonify({"message": "Invalid role"}), 400

    current_user.status = status
    current_user.user_type = role
    db.session.commit()

    return jsonify({"message": "Users approve status and role Updated"}), 200


# Project routes
@api_ta.route("/api/projects", methods=["POST"])
@jwt_required()
def create_project():
    data = request.get_json()

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to create a project"}),
            403,
        )

    new_project = Project(
        name=data["name"],
        statement=data["statement"],
        document_url=data["document_url"],
    )

    db.session.add(new_project)
    db.session.commit()

    return (
        jsonify(
            {"message": "Project created successfully", "project_id": new_project.id}
        ),
        201,
    )


# Milestone routes
@api_ta.route("/api/milestones", methods=["POST"])
@jwt_required()
def create_milestone():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to create a milestone"}),
            403,
        )

    data = request.get_json()

    new_milestone = Milestone(
        name=data["name"],
        description=data["description"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
        max_marks=data["max_marks"],
    )

    db.session.add(new_milestone)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Milestone created successfully",
                "milestone_id": new_milestone.id,
            }
        ),
        201,
    )


# MilestoneStatus routes
@api_ta.route("/api/milestone-status", methods=["POST"])
@jwt_required()
def create_milestone_status():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to create a project"}),
            403,
        )

    data = request.get_json()

    new_status = MilestoneStatus(
        team_id=data["team_id"],
        milestone_id=data["milestone_id"],
        status=data["status"],
        eval_score=data.get("eval_score"),
        eval_feedback=data.get("eval_feedback"),
    )

    if data.get("eval_date"):
        new_status.eval_date = datetime.strptime(data["eval_date"], "%Y-%m-%d")
    if data.get("completed_date"):
        new_status.completed_date = datetime.strptime(
            data["completed_date"], "%Y-%m-%d"
        )

    db.session.add(new_status)
    db.session.commit()

    return jsonify({"message": "Milestone status created successfully"}), 201
