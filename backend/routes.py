
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from datetime import datetime

# Create a Blueprint for the routes
api_bp = Blueprint('api', __name__)

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

# Team routes
@api_bp.route('/api/teams', methods=['POST'])
@jwt_required()
def create_team():
    data = request.get_json()
    
    new_team = Team(
        name=data['name'],
        github_repo_url=data['github_repo_url'],
        team_lead_id=data['team_lead_id']
    )
    
    db.session.add(new_team)
    db.session.commit()
    
    return jsonify({'message': 'Team created successfully', 'team_id': new_team.id}), 201

@api_bp.route('/api/teams/<int:team_id>/members', methods=['POST'])
@jwt_required()
def add_team_member(team_id):
    data = request.get_json()
    team = Team.query.get_or_404(team_id)
    
    if len(team.members) >= 10:
        return jsonify({'message': 'Team is already at maximum capacity'}), 400
        
    user = User.query.get_or_404(data['user_id'])
    user.team_id = team_id
    user.marker2 = True
    
    db.session.commit()
    
    return jsonify({'message': 'Member added to team successfully'}), 200

# Project routes
@api_bp.route('/api/projects', methods=['POST'])
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
@api_bp.route('/api/milestones', methods=['POST'])
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
@api_bp.route('/api/milestone-status', methods=['POST'])
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



@api_bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
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
                
                query = query.filter(getattr(User, field).like(f'{value}%'))
            else:
                
                query = query.filter(getattr(User, field) == value)

    
    users = query.all()

    
    return jsonify([user.to_dict() for user in users]), 200