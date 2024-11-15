from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    github_username = db.Column(db.String(50), unique=True)
    discord_username = db.Column(db.String(50))
    user_type = db.Column(db.Enum('Student', 'TA', 'Admin', 'Instructor', 'Developer', 'Registered', name='user_types'))
    approval_status = db.Column(db.Enum('Active', 'Inactive', 'Decline', name='marker_types'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=True)
    # Relationship to Team (each user belongs to one team)
    team = db.relationship('Team', back_populates='members', foreign_keys=[team_id])

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'github_username': self.github_username,
            'discord_username': self.discord_username,
            'user_type': self.user_type,
            'approval_status': self.approval_status,
            'team_id': self.team_id,
        }


class Team(db.Model):
    __tablename__ = "team"
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    github_repo_url = db.Column(db.String(200))
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    team_lead_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # Relationship to User (each team has many users)
    members = db.relationship('User', back_populates='team', foreign_keys='User.team_id', lazy=True)
    # Relationship to MilestoneStatus
    milestone_statuses = db.relationship('MilestoneStatus', backref='team', lazy=True)

    def to_dict(self):
        return {
            'team_id': self.team_id,
            'id': self.team_id,
            'name': self.team_name,
            'team_name': self.team_name,
            'github_repo_url': self.github_repo_url,
            'project_id': self.project_id,
            'team_lead_id': self.team_lead_id,
            'milestone_statuses': [status.to_dict() for status in self.milestone_statuses],
            'members': [member.to_dict() for member in self.members]
        }


class Member(db.Model):
    __tablename__ = 'member'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
# This Member class might not be needed 

        
class Project(db.Model):
    __tablename__ = "project"
    project_id = db.Column(db.Integer, primary_key=True)
    project_topic = db.Column(db.String(100), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    document_url = db.Column(db.String(200))
    def to_dict(self):
        return {
            'project_id': self.project_id,
            'project_topic': self.project_topic,
            'statement': self.statement,
            'document_url': self.document_url
        }

class Milestone(db.Model):
    __tablename__ = "milestone"
    milestone_id = db.Column(db.Integer, primary_key=True)
    milestone_name = db.Column(db.String(100), nullable=False)
    milestone_description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    max_marks = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    milestone_statuses = db.relationship('MilestoneStatus', backref='milestone', lazy=True)
    def to_dict(self):
        return {
            'milestone_id': self.milestone_id,
            'milestone_name': self.milestone_name,
            'milestone_description': self.milestone_description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'max_marks': self.max_marks,
            'project_id': self.project_id
        }

class MilestoneStatus(db.Model):
    __tablename__ = "milestonestatus"
    milestonestatus_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.milestone_id'), nullable=False)
    milestone_status = db.Column(db.Enum('Evaluated', 'Completed', 'Missed', 'Pending', name='status_types'))
    eval_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    eval_score = db.Column(db.Float)
    eval_feedback = db.Column(db.Text)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.submission_id'))
    def to_dict(self):
        return {
            'milestonestatus_id': self.milestonestatus_id,
            'team_id': self.team_id,
            'milestone_id': self.milestone_id,
            'milestone_status': self.milestone_status,
            'eval_date': self.eval_date,
            'completed_date': self.completed_date,
            'eval_score': self.eval_score,
            'eval_feedback': self.eval_feedback,
            'submission_id': self.submission_id,
        }

class Commit(db.Model):
    __tablename__ = "commit"
    commit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    commit_hash = db.Column(db.String(40), nullable=False)
    commit_message = db.Column(db.Text)
    commit_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    commit_score = db.Column(db.Float, default=0.0)
    commit_url = db.Column(db.String(255))
    commit_clarity = db.Column(db.Float, default=0.0)
    complexity_score = db.Column(db.Float)
    code_quality_score = db.Column(db.Float)
    risk_assessment = db.Column(db.String(20))
    improvement_suggestions = db.Column(db.Text)
    analysis_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    additional_observations = db.Column(db.Text)

    def to_dict(self):
        return {
            'commit_id': self.commit_id,
            'user_id': self.user_id,
            'team_id': self.team_id,
            'commit_hash': self.commit_hash,
            'commit_message': self.commit_message,
            'commit_timestamp': self.commit_timestamp,
            'commit_score': self.commit_score,
            'commit_url': self.commit_url,
            'commit_clarity': self.commit_clarity,
            'complexity_score': self.complexity_score,
            'code_quality_score': self.code_quality_score,
            'risk_assessment': self.risk_assessment,
            'improvement_suggestions': self.improvement_suggestions,
            'analysis_timestamp': self.analysis_timestamp,
            'additional_observations': self.additional_observations,
        }

class Submission(db.Model):
    __tablename__ = "submission"
    submission_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.milestone_id'), nullable=False)
    submission_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            'submission_id': self.submission_id,
            'team_id': self.team_id,
            'milestone_id': self.milestone_id,
            'submission_timestamp': self.submission_timestamp
        }

class File(db.Model):
    __tablename__ = "file"
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.submission_id'), nullable=False)
    def to_dict(self):
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'submission_id': self.submission_id
        }
