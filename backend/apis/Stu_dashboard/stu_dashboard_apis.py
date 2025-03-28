from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Team, MilestoneStatus, Commit, File, Milestone, Milestone, Project
from flask_restx import Resource
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import SQLAlchemyError
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
#UPLOAD_FOLDER = 'uploads'  # Adjust this path as per your application's upload directory
#UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER', 'uploads')  # Adjust this path as per your application's upload directory
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
                'team_score': 0.0,
                'members': [],
                'milestones': [],
                'total_max_marks':0.0
            }
            # Retrieve and add the team's score from milestones
            statuses = MilestoneStatus.query.filter_by(team_id=team.team_id).all()
            team_data['team_score'] = float(sum(status.eval_score or 0 for status in statuses))
            
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
            milestones = Milestone.query.all()
            for milestone in milestones: 
                status = next((s for s in statuses if s.milestone_id == milestone.milestone_id), None) 
                if status: 
                    milestone_status = status.milestone_status 
                    max_marks+=milestone.max_marks
                elif milestone.end_date < datetime.now(): 
                    milestone_status = 'Missed' 
                    max_marks+=milestone.max_marks
                else: 
                    milestone_status = 'Pending'
                milestone_data = {'milestone_name': milestone.milestone_name, 
                                  'milestone_status': milestone_status,
                                  'end_date': milestone.end_date }
                team_data['milestones'].append(milestone_data)
                team_data['total_max_marks'] = float(max_marks)

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
            if 'file' not in request.files or 'milestone_id' not in request.form or 'project_id' not in request.form:
                return createError("submit_project_missing_data", "Missing required data", 400)

            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if current_user.team_id is None:
                return createError("submit_project_no_team", "User is not in a team", 400)
            
            file = request.files['file']
            project_id = request.form['project_id']
            milestone_id = request.form['milestone_id']
            team_id = current_user.team_id #request.form['team_id']
            submission_id = request.form.get('submission_id', None) 
            mark_as_complete = request.form.get(
                'mark_as_complete', 'false').lower() == 'true'
            project = Project.query.get(project_id)
            if(project is None):
                return createError("project_not_found", "Project not found", 400)

            milestone = Milestone.query.get(milestone_id)
            if(milestone is None):
                return createError("milestone_not_found", "Milestone not found", 400)
            

            UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            # Check file validity
            if file and allowed_file(file.filename):
                # Save the file
                filename = secure_filename(
                    f"{current_user_id}_{team_id}_{project_id}_{milestone_id}_{datetime.now().isoformat()}_{file.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                #file_url = f"{request.url_root}uploads/{filename}"
                # Save file details in the database
                new_file = File(file_name=filepath,
                                team_id=team_id, 
                                milestone_id=milestone_id,
                                user_id=current_user_id, 
                                project_id=project_id,
                                submission_id=submission_id)
                db.session.add(new_file)

                # Update MilestoneStatus if marked as complete
                milestone_status = MilestoneStatus.query.filter_by(
                    team_id=team_id, milestone_id=milestone_id).first()
                if milestone_status:
                    if mark_as_complete:
                        milestone_status.submission_status = 'completed'
                # else:
                #     return createError("milestone_status_not_found", "Milestone status not found", 404)

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
            # Query all milestones
            milestones = Milestone.query.all()
            print( milestones)

            if not milestones:
                return jsonify([]), 200 #if no milestone is available, an empty list is returned

            # Format the response data
            response_data = [
                {
                    "milestone_name": milestone.milestone_name,
                    "milestone_description": milestone.milestone_description,
                    "end_date": milestone.end_date.strftime('%d %B') if milestone.end_date else None
                }
                for milestone in milestones
            ]

            return jsonify(response_data), 200

        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return createFatalError("database_error", "Database query failed", str(e)), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return createFatalError("unexpected_error", "An unexpected error occurred", str(e)), 500
