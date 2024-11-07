import unittest
from flask import Flask, json
from flask_testing import TestCase
from main import app, db, User
from unittest.mock import patch

class TestAuthRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('main.github_user_exists', return_value=True)
    def test_register_success(self, mock_github_user_exists):
        response = self.client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'student_email': 'john.doe@example.com',
            'github_username': 'johndoe',
            'discord_username': 'johndoe#1234'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'User registered successfully')

    def test_register_missing_field(self):
        response = self.client.post('/api/auth.register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'student_email': 'john.doe@example.com',
            'github_username': 'johndoe'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing discord_username', response.json['message'])

    def test_register_email_already_registered(self):
        user = User(first_name='Jane', last_name='Doe', password='password123', student_email='jane.doe@example.com', github_username='janedoe', discord_username='janedoe#1234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'student_email': 'jane.doe@example.com',
            'github_username': 'johndoe',
            'discord_username': 'johndoe#1234'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Email already registered')

    def test_register_github_username_already_registered(self):
        user = User(first_name='Jane', last_name='Doe', password='password123', student_email='jane.doe@example.com', github_username='janedoe', discord_username='janedoe#1234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'student_email': 'john.doe@example.com',
            'github_username': 'janedoe',
            'discord_username': 'johndoe#1234'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'GitHub username already registered')

    def test_register_discord_username_already_registered(self):
        user = User(first_name='Jane', last_name='Doe', password='password123', student_email='jane.doe@example.com', github_username='janedoe', discord_username='janedoe#1234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'student_email': 'john.doe@example.com',
            'github_username': 'johndoe',
            'discord_username': 'janedoe#1234'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Discord username already registered')

    def test_register_password_too_short(self):
        response = self.client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'short',
            'student_email': 'john.doe@example.com',
            'github_username': 'johndoe',
            'discord_username': 'johndoe#1234'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Password must be at least 8 characters long')

    @patch('main.github_user_exists', return_value=False)
    def test_register_github_user_does_not_exist(self, mock_github_user_exists):
        response = self.client.post('/api/auth/register', data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'student_email': 'john.doe@example.com',
            'github_username': 'nonexistentuser',
            'discord_username': 'johndoe#1234'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'GitHub username does not exist')

if __name__ == '__main__':
    unittest.main()