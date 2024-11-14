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
@jwt_required()
def get_pending_users():
    try:
        pending_users = User.query.filter_by(approval_status="Inactive").all()
        result = [
            {
                "id": user.user_id,
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
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
@jwt_required()
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
            user.approval_status = "Active"
        elif rejected:
            user.approval_status = "Decline"
        # Update the user's role
        user.user_type = role
        db.session.commit()

    return jsonify({"message": "User approvals processed successfully"}), 200


# (Parag) TAHomePage - Fetching uploads for last 7 days
@api_ta.route("/api/uploads", methods=["GET"])
@jwt_required()
def get_uploads():
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_submissions = (
            db.session.query(Submission)
            .join(Team, Submission.team_id == Team.team_id)
            .filter(Submission.submission_timestamp >= seven_days_ago)
            .all()
        )
        result = [
            {"team": submission.team.team_name} for submission in recent_submissions
        ]
        if not result:
            return jsonify({"message": "No uploads in the last 7 days"}), 200
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error fetching uploads", "error": str(e)}), 500


# (Parag) TAHomePage - Fetching commits for last 7 days
@api_ta.route("/api/commits", methods=["GET"])
@jwt_required()
def get_commits():
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_commits = Commit.query.filter(
            Commit.commit_timestamp >= seven_days_ago
        ).all()
        result = [
            {"team": commit.team.team_name}
            for commit in recent_commits
            if commit.user and commit.user.team
        ]
        if not result:
            return jsonify([{"team": "No commits in the last 7 days"}]), 200
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error fetching commits", "error": str(e)}), 500


# (Parag) TAHomePage - Fetching milestone completions for last 7 days
@api_ta.route("/api/milecomps", methods=["GET"])
@jwt_required()
def get_milecomps():
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_milestone_completions = MilestoneStatus.query.filter(
            MilestoneStatus.completed_date >= seven_days_ago,
            MilestoneStatus.milestone_status == "Completed",
        ).all()
        result = [
            {"team": milestone.team.team_name}
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

# ( Ankush ) Get Milestones
@api_ta.route("/api/milestones", methods=["GET"])
@jwt_required()
def get_milestones():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to read milestones"}),
            403,
        )
    
    milestones = Milestone.query.all()

    return (jsonify([milestone.to_dict() for milestone in milestones]))

# ( Ankush ) Get Milestone
@api_ta.route("/api/milestones/<int:milestone_id>", methods=["GET"])
@jwt_required()
def get_milestone(milestone_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to read milestones"}),
            403,
        )
    
    milestone = Milestone.query.get_or_404(milestone_id)

    return (jsonify(milestone.to_dict()))

# ( Ankush ) Get Milestone Statuses
@api_ta.route("/api/milestone-status", methods=["GET"])
@jwt_required()
def get_milestone_statuses():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to read milestone statuses"}),
            403,
        )
    
    if current_user.user_type == "Student":
        milestone_statuses = MilestoneStatus.query.filter(MilestoneStatus.team_id==current_user.team_id).all()
    else:
        milestone_statuses = MilestoneStatus.query.all()

    return (jsonify([ status.to_dict() for status in milestone_statuses]))


# ( Ankush ) Get Milestone Status
@api_ta.route("/api/milestone-status/<int:milestonestatus_id>", methods=["GET"])
@jwt_required()
def get_milestone_status(milestonestatus_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to read milestone statuses"}),
            403,
        )
    
    if current_user.user_type == "Student":
        data = MilestoneStatus.query.filter(MilestoneStatus.team_id==current_user.team_id, 
                                            MilestoneStatus.milestonestatus_id==milestonestatus_id).first()
        if not data:
            return (
                jsonify({"message": "Milestone Status does not exist!"})
            )
    else:
        milestonestatus = MilestoneStatus.query.get_or_404(milestonestatus_id)

    return (jsonify(milestonestatus.to_dict()))


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


# ( Ankush ) Get TA Dashboard Teams Data
@api_ta.route("/api/ta-teams", methods=["GET"])
@jwt_required()
def get_teams_data_ta():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission fetch teams data."}),
            403,
        )
    
    teams = Team.query.all()

    commits = Commit.query.all()

    milestones = Milestone.query.all()

    milestone_data = { milestone.milestone_id: milestone for milestone in milestones }

    milestone_statuses = MilestoneStatus.query.all()

    dashboard_teams = {}

    for team in teams:
        dashboard_teams[team.team_id] = {
                    "team_id": team.team_id,
                    "team_name": team.team_name,
                    "commits": 0,
                    "score": 0,
                    "total_score": 0,
                    "milestones_completed": 0,
                    "milestones_missed": 0
                }

    for status in milestone_statuses:

        if status.milestone_status == "Evaluated":
            dashboard_teams[status.team_id]['score'] += status.eval_score
            dashboard_teams[status.team_id]['total_score'] += milestone_data[status.milestone_id].max_marks
            dashboard_teams[status.team_id]['milestones_completed'] += 1
        elif status.milestone_status == "Missed":
            dashboard_teams[status.team_id]['score'] += 0
            dashboard_teams[status.team_id]['milestones_missed'] += 1

    for commit in commits:
        dashboard_teams[commit.team_id]['commits'] += 0

    return jsonify({"teams": [dashboard_teams[team] for team in dashboard_teams], "milestones": [milestone.to_dict() for milestone in milestones]})



# ( Ankush ) Get TA Dashboard Team Data
@api_ta.route("/api/ta-team/<int:team_id>", methods=["GET"])
@jwt_required()
def get_team_data_ta(team_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission fetch teams data."}),
            403,
        )
    
    team = Team.query.get_or_404(team_id)

    commits = Commit.query.filter(Commit.team_id==team_id).all()

    members = User.query.filter(User.team_id==team.team_id).all()

    members_data = {member.user_id: {"name": f"{member.first_name} {member.last_name}", "commits": 0} for member in members }

    for commit in commits:
        if commit.user_id in members_data:
            members_data[commit.user_id]['commits'] += 1

    milestones = Milestone.query.all()

    milestone_data = { milestone.milestone_id: {"milestone": milestone.to_dict(), "milestonestatus": ""} for milestone in milestones }

    milestone_statuses = MilestoneStatus.query.filter(MilestoneStatus.team_id==team_id).all()


    for status in milestone_statuses:

        milestone_data[status.milestone_id]['milestonestatus'] = status.to_dict()


    return jsonify({"members": [members_data[member] for member in members_data], "team": team.to_dict(), "milestones": milestone_data})
