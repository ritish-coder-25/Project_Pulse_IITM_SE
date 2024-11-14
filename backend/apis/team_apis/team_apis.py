
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from api_parsers import team_parsers
from marshmallow import ValidationError

# Create a Blueprint for the routes
api_bp_ta = Blueprint('api_bp_teams', __name__)

create_team_schema = team_parsers.CreateTeamSchema()
put_team_schema = team_parsers.PutTeamSchema()

@api_bp_ta.route('/api/teams', methods=['POST'])
@jwt_required()
def create_team_and_add_members():
    try:
        data = create_team_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    #data = request.get_json()
    current_user_id = get_jwt_identity()
    # Create new team
    new_team = Team(
        name=data['team'],
        github_repo_url=data['github_repo_url'],
        team_lead_id=current_user_id,
        project_id=1  # Hardcoded for now
    )

    current_user = User.query.get_or_404(current_user_id)
    current_user.team_id = new_team.id
    
    db.session.add(new_team)
    db.session.commit()
    
    # Add members to the team if provided
    if 'user_ids' in data:
        for member_id in data['user_ids']:
            user = User.query.get_or_404(member_id)
            user.team_id = new_team.id
            db.session.commit()
    
    return jsonify({'message': 'Team created and members added successfully', 'team_id': new_team.id}), 201



@api_bp_ta.route('/api/teams', methods=['GET'])
@jwt_required()
def get_team_and_members():
    query_params = request.args  # Get all query parameters from the URL
    current_user_id = get_jwt_identity()
    team_id = query_params.get('team_id')

    current_user = User.query.get_or_404(current_user_id)
    print(current_user.team.to_dict())
    
    return jsonify({'team': current_user.team.to_dict()}), 200


@api_bp_ta.route('/api/teams', methods=['PUT'])
@jwt_required()
def put_team_and_members():
    try:
        data = put_team_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    #data = request.get_json()  # Get all query parameters from the URL
    current_user_id = get_jwt_identity()

    team_id = data['team_id']
    team = Team.query.get_or_404(team_id)

    if(not team):
        return jsonify({'errorCode': 'put_team_and_members_team_not_found','message': 'Team not found'}), 404
    
    if(int(team.team_lead_id) != int(current_user_id)):
        return jsonify({'errorCode': 'put_team_and_members_only_team_lead_can_edit','message': 'Only Team lead can edit the team'}), 400


    if 'user_ids' in data:
        for member_id in data['user_ids']:
            user = User.query.get_or_404(member_id)
            user.team_id = team.id
            db.session.commit()

    
    return jsonify({'team': team.to_dict()}), 200


@api_bp_ta.route('/api/teams/users', methods=['DELETE'])
@jwt_required()
def delete_members_from_team():
    try:
        query_params = request.args  # Get all query parameters from the URL
        current_user_id = get_jwt_identity()
        team_id = query_params.get('team_id')
        user_id = query_params.get('user_id')

        current_team = Team.query.get_or_404(team_id)
        user = User.query.get(user_id)
        print("team_id", team_id, user_id, current_user_id, "user team", user.team_id, "eq", int(user.team_id) != int(team_id))
        if not user:
                return jsonify({"errorCode": 'delete_members_from_team_user_not_found','message': 'User not found'}), 404

        if not user.team_id or int(user.team_id) != int(team_id):
            return jsonify({"errorCode": 'delete_members_from_team_user_not_in_team','message': 'User is not part of this team'}), 400
        
        if(int(current_team.team_lead_id) == int(user_id)):
            return jsonify({"errorCode": 'delete_members_from_team_no_del_team_lead','message': 'Team lead cannot be removed from the team'}), 400
        
        if(int(current_team.team_lead_id) != int(current_user_id)):
            return jsonify({"errorCode": 'delete_members_from_team_only_team_lead_can_del','message': 'Only Team lead can remove members from the team'}), 400

        if(len(current_team.members) <= 5):
            return jsonify({"errorCode": 'delete_members_from_team_last_member','message': 'Cannot delete members if count is less than 5'}), 400

        user.team_id = None
        db.session.commit()

        return jsonify({'message': 'User removed from team successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"errorCode": "error",'message': 'An error occurred', 'error': str(e)}), 500