from flask import Blueprint, request, jsonify
import os
from flask import send_file, abort
from api_outputs.teams_api.teams_api_output import TeamsDownloadOutput
from flask import send_file, abort
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from models import (
    db,
    User,
    Team,
    Project,
    Milestone,
    MilestoneStatus,
    Commit,
    Submission,
    File,
    File,
)
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import get_jwt_identity

api_ta = Blueprint("api_ta", __name__)

"""
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

"""
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


"""
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
'''
'''
"""


# Project routes
@api_ta.route("/api/projects", methods=["POST"])
@jwt_required()
def create_project():
    if request.is_json:
        data = request.get_json()
        print("Received data:", data)
    else:
        data = request.form

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to create a project"}),
            403,
        )

    new_project = Project(
        project_topic=data["name"],
        statement=data["statement"],
        document_url=data["document_url"],
    )

    db.session.add(new_project)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Project created successfully",
                "project_id": new_project.project_id,
            }
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

#Update Milestones (Ritish)

# Update Milestones (Ritish)
@api_ta.route("/api/milestones/<int:milestone_id>", methods=["PUT"])
@jwt_required()
def update_milestone(milestone_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to update milestone"}),
            403,
        )

    milestone = Milestone.query.get_or_404(milestone_id)
    if "name" in data:
        milestone.milestone_name = data["name"]
    if "description" in data:
        milestone.milestone_description = data["description"]
    if "start_date" in data:
        milestone.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    if "end_date" in data:
        milestone.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
    if "max_marks" in data:
        milestone.max_marks = data["max_marks"]

    db.session.commit()
    return jsonify({"message": "Milestone updated successfully"}), 200


# Delete milestone (Ritish)
@api_ta.route("/api/milestones/<int:milestone_id>", methods=["DELETE"])
@jwt_required()
def delete_milestone(milestone_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify({"message": "You do not have permission to delete milestones"}),
            403,
        )

    milestone = Milestone.query.get_or_404(milestone_id)
    db.session.delete(milestone)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully"}), 200


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

    return jsonify([milestone.to_dict() for milestone in milestones])


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

    return jsonify(milestone.to_dict())


# ( Ankush ) Get Milestone Statuses
@api_ta.route("/api/milestone-status", methods=["GET"])
@jwt_required()
def get_milestone_statuses():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify(
                {"message": "You do not have permission to read milestone statuses"}
            ),
            403,
        )

    if current_user.user_type == "Student":
        milestone_statuses = MilestoneStatus.query.filter(
            MilestoneStatus.team_id == current_user.team_id
        ).all()
    else:
        milestone_statuses = MilestoneStatus.query.all()

    return jsonify([status.to_dict() for status in milestone_statuses])


# ( Ankush ) Get Milestone Status
@api_ta.route("/api/milestone-status/<int:milestonestatus_id>", methods=["GET"])
@jwt_required()
def get_milestone_status(milestonestatus_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ["Admin", "TA", "Instructor", "Developer", "Student"]
    if current_user.user_type not in allowed_roles:
        return (
            jsonify(
                {"message": "You do not have permission to read milestone statuses"}
            ),
            403,
        )

    if current_user.user_type == "Student":
        data = MilestoneStatus.query.filter(
            MilestoneStatus.team_id == current_user.team_id,
            MilestoneStatus.milestonestatus_id == milestonestatus_id,
        ).first()
        if not data:
            return jsonify({"message": "Milestone Status does not exist!"})
    else:
        milestonestatus = MilestoneStatus.query.get_or_404(milestonestatus_id)

    return jsonify(milestonestatus.to_dict())


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


"""
# (Pranjal) Get Files
@api_ta.route("/api/files/<int:team_id>", methods=["GET"])
@jwt_required()
def get_files(team_id):

    # Get all submissions for the team
    submissions = Submission.query.filter_by(team_id=team_id).all()

    documents = []
    for submission in submissions:
        # Get all files for each submission
        files = File.query.filter_by(submission_id=submission.submission_id).all()

        # Get team and milestone names
        team = Team.query.get(submission.team_id)
        milestone = Milestone.query.get(submission.milestone_id)

        # Create document entries for each file
        for file in files:
            document = {
                "id": file.file_id,
                "name": file.file_name,
                "url": f"http://localhost:5000/api/download/{file.file_id}",  # Assuming you have a download endpoint
                "team": team.team_name,
                "milestone": milestone.milestone_name,
            }
            documents.append(document)

    return jsonify({"documents": documents}), 200

"""


"""@api_ta.route("/api/download/<int:file_id>", methods=["GET"])
@jwt_required()
def download_file(file_id):
    try:
        # Get file details from database
        file = File.query.get_or_404(file_id)

        # Construct file path
        file_path = os.path.join("file_submissions", file.file_name)
        ## Filenames are assumed to be saved as filename_fileid_submissionid

        # Check if file exists
        if not os.path.exists(file_path):
            abort(404, description="File not found on server")

        # Return file as attachment
        return send_file(file_path, as_attachment=True, download_name=file.file_name)

    except Exception as e:
        abort(500, description=str(e))
"""

'''
# (Pranjal) Get Files
@api_ta.route("/api/files/<int:team_id>", methods=["GET"])
@jwt_required()
def get_files(team_id):

    # Get all submissions for the team
    submissions = Submission.query.filter_by(team_id=team_id).all()

    documents = []
    for submission in submissions:
        # Get all files for each submission
        files = File.query.filter_by(submission_id=submission.submission_id).all()

        # Get team and milestone names
        team = Team.query.get(submission.team_id)
        milestone = Milestone.query.get(submission.milestone_id)

        # Create document entries for each file
        for file in files:
            document = {
                "id": file.file_id,
                "name": file.file_name,
                "url": f"http://localhost:5000/api/download/{file.file_id}",  # Assuming you have a download endpoint
                "team": team.team_name,
                "milestone": milestone.milestone_name,
            }
            documents.append(document)

    return jsonify({"documents": documents}), 200


    return jsonify(
        {
            "members": [members_data[member] for member in members_data],
            "team": team.to_dict(),
            "milestones": milestone_data,
        }
    )
'''
@api_ta.route("/api/download/<int:file_id>", methods=["GET"])
@jwt_required()
def download_file(file_id):
    """Download a submitted file by file ID.
    
    Args:
        file_id (int): The ID of the file to download
        
    Returns:
        file: The requested file as an attachment
        
    Raises:
        404: If file not found in database or on server
        500: If there is a server error
    ---

    """
    try:
        # Get file details from database
        file = File.query.get_or_404(file_id)

        # Construct file path
        file_path = os.path.join("file_submissions", file.file_name)
        ## Filenames are assumed to be saved as filename_fileid_submissionid

        # Check if file exists
        if not os.path.exists(file_path):
            abort(404, description="File not found on server")

        # Return file as attachment
        return send_file(file_path, as_attachment=True, download_name=file.file_name)

    except Exception as e:
        abort(500, description=str(e))


# (Pranjal) Get Files
@api_ta.route("/api/files/<int:team_id>", methods=["GET"])
@jwt_required()
def get_files(team_id):

    # Get all submissions for the team
    submissions = Submission.query.filter_by(team_id=team_id).all()

    documents = []
    for submission in submissions:
        # Get all files for each submission
        files = File.query.filter_by(submission_id=submission.submission_id).all()

        # Get team and milestone names
        team = Team.query.get(submission.team_id)
        milestone = Milestone.query.get(submission.milestone_id)

        # Create document entries for each file
        for file in files:
            document = {
                "id": file.file_id,
                "name": file.file_name,
                "url": f"http://localhost:5000/api/download/{file.file_id}",  # Assuming you have a download endpoint
                "team": team.team_name,
                "milestone": milestone.milestone_name,
            }
            documents.append(document)

    return jsonify({"documents": documents}), 200




@api_ta.route("/api/download/<int:file_id>", methods=["GET"])
@jwt_required()
def download_file(file_id):
    try:
        # Get file details from database
        file = File.query.get_or_404(file_id)

        # Construct file path
        file_path = os.path.join("file_submissions", file.file_name)
        ## Filenames are assumed to be saved as filename_fileid_submissionid

        # Check if file exists
        if not os.path.exists(file_path):
            abort(404, description="File not found on server")

        # Return file as attachment
        return send_file(file_path, as_attachment=True, download_name=file.file_name)

    except Exception as e:
        abort(500, description=str(e))
'''
'''
