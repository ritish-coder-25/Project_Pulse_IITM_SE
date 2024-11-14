from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Milestone, Submission, File
from datetime import datetime
import os

student_dashboard = Blueprint('student_dashboard', __name__)

# Helper function to create an upload directory


def get_upload_path(student_id, milestone_id):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    student_folder = os.path.join(upload_folder, f"student_{student_id}")
    milestone_folder = os.path.join(
        student_folder, f"milestone_{milestone_id}")
    os.makedirs(milestone_folder, exist_ok=True)
    return milestone_folder

# Endpoint to fetch milestone deadlines


@student_dashboard.route('/api/milestones', methods=['GET'])
@jwt_required()
def get_milestones():
    milestones = Milestone.query.all()
    response = [
        {"id": m.id, "name": m.name, "due_date": m.due_date,
            "description": m.description}
        for m in milestones
    ]
    return jsonify(response), 200

# Endpoint to fetch the student's milestone statuses


@student_dashboard.route('/api/student/milestones', methods=['GET'])
@jwt_required()
def get_student_milestones():
    student_id = get_jwt_identity()
    milestones = Milestone.query.all()
    response = []
    for milestone in milestones:
        submission = Submission.query.filter_by(
            student_id=student_id, milestone_id=milestone.id).first()
        status = "Not open" if datetime.now() < milestone.due_date else "Due Date missed"
        completed = False
        if submission:
            status = f"Completed on {submission.completed_date}" if submission.completed else "Submitted, Pending Completion"
            completed = submission.completed
        response.append({
            "id": milestone.id,
            "name": milestone.name,
            "due_date": milestone.due_date,
            "status": status,
            "completed": completed
        })
    return jsonify(response), 200

# Endpoint to upload a file for a specific milestone


@student_dashboard.route('/api/student/milestones/<int:milestone_id>/upload', methods=['POST'])
@jwt_required()
def upload_file(milestone_id):
    student_id = get_jwt_identity()
    milestone = Milestone.query.get_or_404(milestone_id)

    if datetime.now() > milestone.due_date:
        return jsonify({"message": "Milestone deadline has passed."}), 400

    file = request.files.get('file')
    if not file:
        return jsonify({"message": "No file provided."}), 400

    filename = secure_filename(file.filename)
    upload_path = get_upload_path(student_id, milestone_id)
    file_path = os.path.join(upload_path, filename)
    file.save(file_path)

    new_file = File(milestone_id=milestone_id,
                    student_id=student_id, file_path=file_path)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully."}), 200

# Endpoint to mark milestone as complete


@student_dashboard.route('/api/student/milestones/<int:milestone_id>/complete', methods=['POST'])
@jwt_required()
def mark_as_complete(milestone_id):
    student_id = get_jwt_identity()
    submission = Submission.query.filter_by(
        student_id=student_id, milestone_id=milestone_id).first()

    if submission and submission.completed:
        return jsonify({"message": "Milestone already completed."}), 400

    if not submission:
        submission = Submission(student_id=student_id, milestone_id=milestone_id,
                                completed=True, completed_date=datetime.now())
        db.session.add(submission)
    else:
        submission.completed = True
        submission.completed_date = datetime.now()
    db.session.commit()

    return jsonify({"message": "Milestone marked as complete."}), 200

# Endpoint to submit all milestones


@student_dashboard.route('/api/student/milestones/submit', methods=['POST'])
@jwt_required()
def submit_milestones():
    student_id = get_jwt_identity()
    milestones = Milestone.query.all()
    for milestone in milestones:
        submission = Submission.query.filter_by(
            student_id=student_id, milestone_id=milestone.id).first()
        if submission and not submission.completed:
            submission.completed = True
            submission.completed_date = datetime.now()
    db.session.commit()

    return jsonify({"message": "All milestones submitted successfully."}), 200
