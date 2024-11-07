
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

api_ta = Blueprint('api_ta', __name__)

@api_ta.route('/api/users_allocate', methods=['POST'])
@jwt_required()
def allocate_users():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ['Admin', 'TA', 'Instructor', 'Developer']
    if current_user.user_type not in allowed_roles:
        return jsonify({'message': 'You do not have permission to approve users'}), 403
    
    team_id = data['team_id']
    users = data['users']

    for user_id in users:
        user = User.query.get(user_id)
        user.team_id = team_id
        db.session.commit()

    return jsonify({'message': 'Users allocated to team successfully'}), 200


@api_ta.route('/api/users_approval', methods=['POST'])
@jwt_required()
def approve_users():

    data = request.get_json()

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ['Admin', 'TA', 'Instructor', 'Developer']
    if current_user.user_type not in allowed_roles:
        return jsonify({'message': 'You do not have permission to approve users'}), 403
    
    status = data['status']
    role = data['role']

    if status not in ['Active', 'Inactive', 'Decline']:
        return jsonify({'message': 'Invalid status'}), 400
    if role not in ['Student', 'TA', 'Admin', 'Instructor', 'Developer']:
        return jsonify({'message': 'Invalid role'}), 400
    
    current_user.status =status
    current_user.user_type = role
    db.session.commit()




    return jsonify({'message': 'Users approve status and role Updated'}), 200


# Project routes
@api_ta.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ['Admin', 'TA', 'Instructor', 'Developer']
    if current_user.user_type not in allowed_roles:
        return jsonify({'message': 'You do not have permission to create a project'}), 403

    
    new_project = Project(
        name=data['name'],
        statement=data['statement'],
        document_url=data['document_url']
    )
    
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'message': 'Project created successfully', 'project_id': new_project.id}), 201

# Milestone routes
@api_ta.route('/api/milestones', methods=['POST'])
@jwt_required()
def create_milestone():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ['Admin', 'TA', 'Instructor', 'Developer']
    if current_user.user_type not in allowed_roles:
        return jsonify({'message': 'You do not have permission to create a milestone'}), 403
        

    data = request.get_json()
    
    new_milestone = Milestone(
        name=data['name'],
        description=data['description'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d'),
        max_marks=data['max_marks']
    )
    
    db.session.add(new_milestone)
    db.session.commit()
    
    return jsonify({'message': 'Milestone created successfully', 'milestone_id': new_milestone.id}), 201

# MilestoneStatus routes
@api_ta.route('/api/milestone-status', methods=['POST'])
@jwt_required()
def create_milestone_status():

    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    allowed_roles = ['Admin', 'TA', 'Instructor', 'Developer']
    if current_user.user_type not in allowed_roles:
        return jsonify({'message': 'You do not have permission to create a project'}), 403
        

    data = request.get_json()
    
    new_status = MilestoneStatus(
        team_id=data['team_id'],
        milestone_id=data['milestone_id'],
        status=data['status'],
        eval_score=data.get('eval_score'),
        eval_feedback=data.get('eval_feedback')
    )
    
    if data.get('eval_date'):
        new_status.eval_date = datetime.strptime(data['eval_date'], '%Y-%m-%d')
    if data.get('completed_date'):
        new_status.completed_date = datetime.strptime(data['completed_date'], '%Y-%m-%d')
    
    db.session.add(new_status)
    db.session.commit()
    
    return jsonify({'message': 'Milestone status created successfully'}), 201
