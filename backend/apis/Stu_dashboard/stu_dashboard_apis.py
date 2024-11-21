from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Team, MilestoneStatus, Commit, File, Milestone, Milestone
from flask_restx import Resource
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
from datetime import datetime
import os
from api_outputs.api_outputs_common import CommonErrorSchema, CommonErrorErrorSchemaFatal
from api_outputs.teams_api.teams_stuDash_output import StuDashTeamSchema, MilestoneDeadlineSchema, SubmitProjectResponseSchema
from helpers.ErrorCommonHelpers import createError, createFatalError
from flask_restx import fields

# Blueprint for Student Dashboard API
api_bp_stu = Blueprint("Student Dashboard APIs", "Student Dashboard",
                       description="Display of Student dashboard")

# Constants
UPLOAD_FOLDER = 'uploads'  # Adjust this path as per your application's upload directory
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'zip'}


def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp_stu.route('/api/stu_home/<int:stu_id>')
class StuDashboard(Resource):
    @api_bp_stu.response(201, StuDashTeamSchema)
    @api_bp_stu.response(404, CommonErrorSchema)
    @api_bp_stu.response(500, CommonErrorSchema)
    @jwt_required()
    def get(self, stu_id):
        """Retrieve information about a student's team, providing an overview of the student's team activities and progress."""
        try:
            current_user = User.query.get_or_404(stu_id)
            print (current_user)
            if not current_user.team_id:
                return createError("team_get_curr_no_team", "User is not in a team", 404)
            
            team = Team.query.get_or_404(current_user.team_id)
            print (team)
            
            team_data = {
                'user_name': f"{current_user.first_name} {current_user.last_name}",
                'team_name': team.team_name,
                'team_score': 0,
                'members': [],
                'milestones': [],
                'total_max_marks':0
            }
            # Retrieve and add the team's score from milestones
            statuses = MilestoneStatus.query.filter_by(team_id=team.team_id).all()
            team_data['team_score'] = sum(status.eval_score or 0 for status in statuses)
            
            # Retrieve member data for the team, including commit counts
            for member in team.members:
                member_data = {
                    'name': f"{member.first_name} {member.last_name}",
                    'email': member.email,
                    'commit_count': Commit.query.filter_by(user_id=member.user_id).count()
                }
                print(member_data)
                team_data['members'].append(member_data)

            # Fetch milestone details
            max_marks=0
            for status in statuses:
                milestone = Milestone.query.get(status.milestone_id)
                if milestone:
                    max_marks += milestone.max_marks
                    milestone_data = {
                        'milestone_name': milestone.milestone_name,
                        'milestone_status': status.milestone_status,
                        'end_date': milestone.end_date,
                    }
                    team_data['milestones'].append(milestone_data)
                    team_data['total_max_marks'] = max_marks
            print(team_data)

            return jsonify(team_data), 200
        except NotFound as e:
            return createError("user_not_found", "User not found", 404)
        except Exception as e: 
            db.session.rollback() 
            return createError("unknown_error", "An error occurred", 500)
        

@api_bp_stu.route('/api/submit_project')
class SubmitProject(Resource):
    @api_bp_stu.response(201, SubmitProjectResponseSchema)
    @api_bp_stu.response(400, CommonErrorSchema)
    @jwt_required()
    def post(self):
        """Handle project file submissions, save file details and optionally mark the milestone as complete for a student. """
        try:
            # Ensure required data is present
            if 'file' not in request.files or 'student_id' not in request.form or 'project_id' not in request.form:
                return createError("submit_project_missing_data", "Missing required data", 400)

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
                    return createError("milestone_status_not_found", "Milestone status not found", 404)

                db.session.commit()
                return jsonify({'message': 'Project submitted successfully', 'file_path': filepath}), 201

            return createError("invalid_file_type", "Invalid file type", 400)

        except Exception as e:
            db.session.rollback()
            return createFatalError("submit_project_error", "An error occurred", str(e))


@api_bp_stu.route('/api/milestones/deadlines')
class MilestoneDeadlines(Resource):
    @api_bp_stu.response(200, MilestoneDeadlineSchema(many=True))
    @api_bp_stu.response(400, CommonErrorSchema)
    @jwt_required()
    def get(self):
        """Retrieve and return a list of all milestones with their names, descriptions, and deadlines."""
        try:
            # Query all milestones and get their name, description, and end date
            milestones = Milestone.query.all()

            # Format the response data
            response_data = [
                {
                    "milestone_name": milestone.milestone_name,
                    "milestone_description": milestone.description,
                    "end_date": milestone.end_date.strftime('%d %B')
                }
                for milestone in milestones
            ]

            return jsonify(response_data), 200

        except Exception as e:
            print(f"Error fetching milestones: {e}")
            return createFatalError("milestone_fetch_error", "Unable to fetch milestone deadlines", str(e))
