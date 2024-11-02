from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100), unique=True, nullable=False)
    github_username = db.Column(db.String(50), unique=True)
    discord_username = db.Column(db.String(50))
    user_type = db.Column(db.Enum('Student', 'TA', 'Admin', 'Instructor', 'Developer','Registered', name='user_types'))
    status = db.Column(db.Enum('Active', 'Inactive', 'Decline', name='marker_types'), nullable=True)
    allocation_status = db.Column(db.Boolean, default=False)  # True if allocated to a team
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    commits = db.relationship('Commit', backref='user', lazy=True)

    def to_dict(self):
        return {
        'id': self.id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'student_email': self.student_email,
        'github_username': self.github_username,
        'discord_username': self.discord_username,
        'user_type': self.user_type,
        'status': self.status,
        'allocation_status': self.allocation_status,
        'team_id': self.team_id
        }

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    github_repo_url = db.Column(db.String(200))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    
    team_lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    milestone_statuses = db.relationship('MilestoneStatus', backref='team', lazy=True)
    members = db.relationship('User', 
                               backref='team', 
                               lazy=True, 
                               foreign_keys=[User.team_id])

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    document_url = db.Column(db.String(200))
    teams = db.relationship('Team', backref='project', lazy=True)

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    max_marks = db.Column(db.Float, nullable=False)
    milestone_statuses = db.relationship('MilestoneStatus', backref='milestone', lazy=True)

class MilestoneStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.id'), nullable=False)
    status = db.Column(db.Enum('Evaluated', 'Completed', 'Missed', 'Pending', name='status_types'))
    eval_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    eval_score = db.Column(db.Float)
    eval_feedback = db.Column(db.Text)

class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commit_hash = db.Column(db.String(40), nullable=False)
    commit_message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    commit_score = db.Column(db.Float, default=0.0)
    commit_url = db.Column(db.String(255))
    analysis = db.relationship('CommitAnalysis', back_populates='commit', uselist=False, passive_deletes=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'commit_hash': self.commit_hash,
            'commit_message': self.commit_message,
            'timestamp': self.timestamp,
            'analysis': self.analysis.to_dict() if self.analysis else None,  # Include analysis data if it exists
        }

class CommitAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.Integer, db.ForeignKey('commit.id'), nullable=False)
    commit_clarity = db.Column(db.Float)  # Score between 0-10
    complexity_score = db.Column(db.Float)  # Numerical score for complexity
    code_quality_score = db.Column(db.Float)  # Score between 0-100
    risk_assessment = db.Column(db.String(20))  # e.g., 'low', 'medium', 'high'
    improvement_suggestions = db.Column(db.Text)  # Text field for suggestions
    analysis_timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Analysis timestamp
    additional_observations = db.Column(db.Text)  # Text field for observations

    commit = db.relationship('Commit', back_populates='analysis')

    def to_dict(self):
        return {
            'id': self.id,
            'commit_id': self.commit_id,
            'commit_clarity': self.commit_clarity,
            'complexity_score': self.complexity_score,
            'code_quality_score': self.code_quality_score,
            'risk_assessment': self.risk_assessment,
            'improvement_suggestions': self.improvement_suggestions,
            'analysis_timestamp': self.analysis_timestamp,
            'additional_observations': self.additional_observations,
        }

