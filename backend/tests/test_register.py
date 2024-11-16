import unittest
from flask import Flask, json
from flask_testing import TestCase
from main import app, db, User
from unittest.mock import patch
from github_mock import mock_github_user_exists





#@patch('main.github_user_exists', return_value=True)
def test_register_success(client, mock_github_user_exists):
    mock_github_user_exists.return_value = True
    response = client.post('/api/auth/register', data=json.dumps({
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'email': 'john.doe@example.com',
        'github_username': 'johndoe',
        'discord_username': 'johndoe#1234'
    }), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'


def test_register_missing_field(client):
        response = client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'email': 'john.doe1@example.com',
            'github_username': 'johndoe'
        }), content_type='application/json')

        assert response.status_code == 400
        assert 'Missing discord_username' in response.json['message']

def test_register_email_already_registered(client):
    user = User(first_name='Jane', last_name='Doe', password='password123', email='jane.doe2@example.com', github_username='janedoe1', discord_username='janedoe#1234')
    db.session.add(user)
    db.session.commit()
    response = client.post('/api/auth/register', data=json.dumps({
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'email': 'jane.doe2@example.com',
        'github_username': 'johndoe',
        'discord_username': 'johndoe#1234'
    }), content_type='application/json')
    assert response.status_code ==400
    assert response.json['message'] == 'Email already registered'

def test_register_github_username_already_registered(client):
    user = User(first_name='Jane', last_name='Doe', password='password123', email='jane.doe3@example.com', github_username='janedoe2', discord_username='janedoe#1234')
    db.session.add(user)
    db.session.commit()
    response = client.post('/api/auth/register', data=json.dumps({
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'email': 'john.doe4@example.com',
        'github_username': 'janedoe2',
        'discord_username': 'johndoe#1234'
    }), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'GitHub username already registered'
def test_register_discord_username_already_registered(client):
    user = User(first_name='Jane', last_name='Doe', password='password123', email='jane.doe5@example.com', github_username='janedoe3', discord_username='janedoe#1234')
    db.session.add(user)
    db.session.commit()
    response = client.post('/api/auth/register', data=json.dumps({
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'email': 'john.doe6@example.com',
        'github_username': 'johndoe4',
        'discord_username': 'janedoe#1234'
    }), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'Discord username already registered'
def test_register_password_too_short(client):
    response = client.post('/api/auth/register', data=json.dumps({
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'short',
        'email': 'john.doe7@example.com',
        'github_username': 'johndoe5',
        'discord_username': 'johndoe#12341'
    }), content_type='application/json')
    assert response.status_code == 400
    assert response.json['message'] == 'Password must be at least 8 characters long'
#@patch('main.github_user_exists', return_value=False)
def test_register_github_user_does_not_exist(client, mock_github_user_exists):
    mock_github_user_exists.return_value = True
    response = client.post('/api/auth/register', data=json.dumps({
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'email': 'john.doe8@example.com',
        'github_username': 'nonexistentuser',
        'discord_username': 'johndoe#12345'
    }), content_type='application/json')
    assert (response.status_code == 400)
    assert (response.json['message'] == 'GitHub username does not exist')