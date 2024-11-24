import json
import pytest
from main import app, db, User, Team, Project
from unittest.mock import patch
from db_test_helpers import get_user_token_header, db_create_student_user, db_create_milestone



def test_submit_project_valid(client, create_team_with_users, auth_headers, sample_file):
    team, team_users, team_lead = create_team_with_users
    new_headers = get_user_token_header(team_lead.user_id)
    milestone = db_create_milestone(db,1)
    data = {
        'milestone_id': milestone.milestone_id,
        'project_id': 1,
        'file': sample_file
    }
    response = client.post(
        '/api/submit_project',
        data=data,
        headers=new_headers,
        content_type='multipart/form-data'
    )
    print(response.get_json())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Project submitted successfully'
    assert data['file_path'] is not None
    print(data['file_path'])


#@patch('apis.stu_dashboard_apis.some_dependency', autospec=True)  # Replace with actual dependencies if any
def test_submit_project_project_not_exists(db,client, sample_file):
    user, password = db_create_student_user(db, team_id=1)
    new_headers = get_user_token_header(user.user_id)
    data = {
        'milestone_id': '556',
        'project_id': '67890',
        'file': sample_file
    }
    response = client.post(
        '/api/submit_project',
        data=data,
        headers=new_headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == 'project_not_found'

def test_submit_project_milestone_not_exists(client, auth_headers, sample_file):
    user, password = db_create_student_user(db, team_id=1)
    new_headers = get_user_token_header(user.user_id)
    data = {
        'milestone_id': '12345',
        'project_id': 1,
        'file': sample_file
    }
    response = client.post(
        '/api/submit_project',
        data=data,
        headers=new_headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == 'milestone_not_found'

def test_submit_project_invalid_file_type(db,client, sample_file_invalid):
    user, password = db_create_student_user(db, team_id=1)
    new_headers = get_user_token_header(user.user_id)
    data = {
        'milestone_id': 1,
        'project_id': 1,
        'file': sample_file_invalid
    }
    response = client.post(
        '/api/submit_project',
        data=data,
        headers=new_headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == 'invalid_file_type'

def test_submit_project_missing_file(client, auth_headers):
    data = {
        'student_id': '12345',
        'project_id': '67890',
        # 'file' is missing
    }
    response = client.post(
        '/api/submit_project',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == 'submit_project_missing_data'
    assert 'message' in data
    assert data['message'] == 'Missing required data'
