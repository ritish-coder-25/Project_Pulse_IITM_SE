
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from api_parsers import team_parsers
from marshmallow import ValidationError
from flask_smorest import Api, Blueprint, abort
from flask.views import MethodView
# Create a Blueprint for the routes
api_bp = Blueprint('api', __name__)
api_bp_users = Blueprint("api_bp_users", "Users", description="Operations on users")

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





