
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from api_parsers import team_parsers
from marshmallow import ValidationError
from flask_smorest import Api, Blueprint, abort
from flask.views import MethodView
import os
# Create a Blueprint for the routes
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'pdf', 'zip'}

api_bp = Blueprint('api', __name__)
api_bp_users = Blueprint("api_bp_users", "Users", description="Operations on users")


# Utility function to check file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# User routes
# @api_bp.route('/api/users', methods=['GET'])
# @jwt_required()
# def get_users():
#     users = User.query.all()
#     return jsonify([{
#         'id': user.id,
#         'first_name': user.first_name,
#         'last_name': user.last_name,
#         'student_email': user.student_email,
#         'user_type': user.user_type,
#         'marker': user.marker
#     } for user in users]), 200
## Team routes


# Commit routes
@api_bp.route('/api/commits', methods=['POST'])
@jwt_required()
def record_commit():
    data = request.get_json()

    new_commit = Commit(
        user_id=data['user_id'],
        commit_hash=data['commit_hash'],
        commit_message=data['commit_message']
    )
    
    db.session.add(new_commit)
    db.session.commit()
    
    return jsonify({'message': 'Commit recorded successfully'}), 201

@api_bp_users.route('/api/users', methods=['GET'])
class UserResource(MethodView):
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

#(Joyce) Student Home component API 
@api_bp.route('/api/stu_home/<int:stu_id>', methods=['GET'])
@jwt_required()
def get_stuhome(stu_id):
    user = User.query.get(stu_id)
    if user:
        team = Team.query.get(user.team_id)
        if team:
            # Construct team data with members' names, emails, and their commits
            team_data = {
                'team_name': team.team_name,
                'members': []
            }

            # Loop through each member in the team
            for member in team.members:
                member_data = {
                    'name': f"{member.first_name} {member.last_name}",
                    'email': member.email,
                    'commit_count': 0,
                }

                # Get commits for each member
                member_commits = Commit.query.filter_by(user_id=member.user_id).all()
                member_data['commit_count'] = len(member_commits)  # Count of commits

                team_data['members'].append(member_data)

            return jsonify(team_data), 200
        else:
            return jsonify({"error": "No Team Found"}), 404
    else:
        return jsonify({"error": "User not found"}), 404


@api_bp.route('/api/submit_project', methods=['POST'])
@jwt_required()
def submit_project():
    # Ensure required data is present
    if 'file' not in request.files or 'student_id' not in request.form or 'project_id' not in request.form:
        return jsonify({'error': 'Missing required data'}), 400

    file = request.files['file']
    student_id = request.form['student_id']
    project_id = request.form['project_id']
    mark_as_complete = request.form.get(
        'mark_as_complete', 'false').lower() == 'true'

    # Check file validity
    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(
            f"{student_id}_{project_id}_{datetime.now().isoformat()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Save file details in the database
        new_file = File(file_name=filepath,
                        student_id=student_id, project_id=project_id)
        db.session.add(new_file)

        # Update MilestoneStatus if marked as complete
        milestone_status = MilestoneStatus.query.filter_by(
            student_id=student_id, project_id=project_id).first()
        if milestone_status:
            if mark_as_complete:
                milestone_status.submission_status = 'completed'
        else:
            return jsonify({'error': 'Milestone status not found'}), 404

        db.session.commit()
        return jsonify({'message': 'Project submitted successfully', 'file_path': filepath}), 201

    return jsonify({'error': 'Invalid file type'}), 400

# New route to fetch milestone details for deadlines


@api_bp.route('/api/milestones/deadlines', methods=['GET'])
@jwt_required()
def get_milestone_deadlines():
    try:
        # Query all milestones and get their name, description, and end date
        milestones = Milestone.query.all()

        # Format the response data
        response_data = [
            {
                "milestone_name": milestone.name,
                "milestone_description": milestone.description,
                # Format date as in the example image
                "end_date": milestone.end_date.strftime('%d %B')
            }
            for milestone in milestones
        ]

        # Return JSON response
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error fetching milestones: {e}")
        return jsonify({"error": "Unable to fetch milestone deadlines"}), 500

