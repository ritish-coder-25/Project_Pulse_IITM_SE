
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

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
## Team routes

@api_bp.route('/api/teams', methods=['POST'])
@jwt_required()
def create_team_and_add_members():
    data = request.get_json()
    
    # Create new team
    new_team = Team(
        name=data['name'],
        github_repo_url=data['github_repo_url'],
        team_lead_id=data['team_lead_id']
    )
    
    db.session.add(new_team)
    db.session.commit()
    
    # Add members to the team if provided
    if 'members' in data:
        for member_id in data['members']:
            user = User.query.get_or_404(member_id)
            user.team_id = new_team.id
            db.session.commit()
    
    return jsonify({'message': 'Team created and members added successfully', 'team_id': new_team.id}), 201

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

#(Joyce) Student Home component API 
@api_bp.route('/api/stu_home/<int:stu_id>', methods=['GET'])
@jwt_required()
def get_stuhome(stu_id):
    user = User.query.get(stu_id)
    if user:
        team = Team.query.get(user.team_id)
        if team:
            # team data with members' names, emails, and their commits
            team_data = {
                'team_name': team.team_name,
                'team_score': 0,
                'members': []
            }
            scores = MilestoneStatus.query.filter_by(team_id=team.team_id).all() 
            for score in scores: 
                team_data['team_score'] += score.eval_score

            for member in team.members:
                member_data = {
                    'name': f"{member.first_name} {member.last_name}",
                    'email': member.email,
                    'commit_count': 0,
                }

                member_commits = Commit.query.filter_by(user_id=member.user_id).all()
                member_data['commit_count'] = len(member_commits)  # Count of commits

                team_data['members'].append(member_data)

            return jsonify(team_data), 200
        else:
            return jsonify({"error": "No Team Found"}), 404
    else:
        return jsonify({"error": "User not found"}), 404



