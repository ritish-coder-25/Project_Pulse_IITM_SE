import json
import pytest
from main import app, db, User, Team, Project
from unittest.mock import patch



@patch('apis.user_apis.userAuthentication.bcrypt', autospec=True)
def test_login_student_success(mock_bcrypt,client, create_student_user):
    mock_bcrypt.check_password_hash.return_value = True
    user, password = create_student_user
    response = client.post('/api/auth/login', data=json.dumps({
        'email': user.email,
        'password': password
    }), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['email'] == user.email
    assert data['access_token'] is not None
    mock_bcrypt.check_password_hash.assert_called_once_with(user.password, password)


@patch('apis.user_apis.userAuthentication.bcrypt', autospec=True)
def test_login_ta_success(mock_bcrypt,client, create_ta_user):
    mock_bcrypt.check_password_hash.return_value = True
    user, password = create_ta_user
    response = client.post('/api/auth/login', data=json.dumps({
        'email': user.email,
        'password': password
    }), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['email'] == user.email
    assert data['access_token'] is not None
    mock_bcrypt.check_password_hash.assert_called_once_with(user.password, password)


@patch('apis.user_apis.userAuthentication.bcrypt', autospec=True)
def test_login_wrong_password_success(mock_bcrypt,client, create_ta_user):
    mock_bcrypt.check_password_hash.return_value = False
    user, password = create_ta_user
    response = client.post('/api/auth/login', data=json.dumps({
        'email': user.email,
        'password': "password"
    }), content_type='application/json')
    assert response.status_code == 401
    data = response.get_json()
    assert data['errorCode'] == "invalid_login"
    assert 'access_token' not in data
    mock_bcrypt.check_password_hash.assert_called_once_with(user.password, "password")
