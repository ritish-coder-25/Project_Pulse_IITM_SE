from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from config import Config
from routes import api_bp
from ta_routes import api_ta
from utils.github_helpers import github_user_exists
import logging

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(api_bp)
app.register_blueprint(api_ta)


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'password', 'student_email', 'github_username', 'discord_username']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing {field}'}), 400
    
    if User.query.filter_by(student_email=data['student_email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    if User.query.filter_by(github_username=data['github_username']).first():
        return jsonify({'message': 'GitHub username already registered'}), 400
    
    if User.query.filter_by(discord_username=data['discord_username']).first():
        return jsonify({'message': 'Discord username already registered'}), 400
        
    if len(data['password']) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400
    
    if not github_user_exists(data['github_username']):
        return jsonify({'message': 'GitHub username does not exist'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=hashed_password,
        student_email=data['student_email'],
        github_username=data['github_username'],
        discord_username=data['discord_username'],
        user_type='Registered',
        status='Inactive',
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(student_email=data['student_email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
        
    return jsonify({'message': 'Invalid credentials'}), 401




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database created successfully.")
        except Exception as e:
            logging.error(f"Error creating database: {e}")
    app.run(debug=True)


    # Create default admin user if not exists
    with app.app_context():
        if not User.query.filter_by(email='admin@projectpulse.com').first():
            admin_user = User(
                first_name='Admin',
                last_name='ProjectPulse',
                password=bcrypt.generate_password_hash('projectpulse123').decode('utf-8'),
                email='admin@projectpulse.com',
                github_username='pranjalkar99',
                discord_username='test123',
                user_type='Admin',
                approval_status='Active',
            )
            db.session.add(admin_user)
            db.session.commit()
            logging.info("Default admin user created.")
        else:
            logging.info("Default admin user already exists.")