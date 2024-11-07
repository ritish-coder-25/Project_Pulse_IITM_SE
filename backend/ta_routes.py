
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