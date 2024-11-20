from flask import jsonify
from flask_jwt_extended import jwt_required
from models import db, Commit, Team, User, Submission, MilestoneStatus
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.commits_api.TADcommits_api_outputs import TACommitsResponse
from api_outputs.submissions_api.TADuploads_api_outputs import UploadsResponse
from api_outputs.project_api.TADmilestone_api_outputs import (
    MilestoneCompletionsResponse,
)
from datetime import datetime, timedelta, timezone
from helpers.ErrorCommonHelpers import createError, createFatalError

api_bp_tahome = Blueprint(
    "Fetch TAHomepage APIs",
    "Fetch TAHomepage",
    description="Operations for getting last 7 day's activity for TA Homepage",
)


@api_bp_tahome.route("/api/commits")
class CommitsResource(Resource):
    @jwt_required()
    @api_bp_tahome.response(200, TACommitsResponse)
    def get(self):
        """Get teams who have done commits in last 7 days"""
        try:
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

            recent_commits = (
                db.session.query(Commit, Team.team_name)
                .join(
                    Team, Commit.team_id == Team.team_id
                )  # Join with Team using team_id
                .join(
                    User, Commit.user_id == User.user_id
                )  # Join with User to ensure user exists
                .filter(Commit.commit_timestamp >= seven_days_ago)
                .all()
            )

            # Build the result from the query
            result = [{"team": team_name} for commit, team_name in recent_commits]

            if not result:
                return (
                    jsonify(
                        {
                            "team": "No commits in the last 7 days",
                        }
                    ),
                    200,
                )

            return jsonify(result), 200
        except Exception as e:
            return createFatalError(
                "commits_fetching_error", "Error fetching commits", str(e)
            )


@api_bp_tahome.route("/api/project/milecomps")
class MilestoneCompletionsResource(Resource):
    @jwt_required()
    @api_bp_tahome.response(200, MilestoneCompletionsResponse)
    def get(self):
        """Get teams who have marked milestones as completed in last 7 days"""
        try:
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

            recent_milestone_completions = MilestoneStatus.query.filter(
                MilestoneStatus.completed_date >= seven_days_ago,
                MilestoneStatus.milestone_status == "Completed",
            ).all()

            result = [
                {"team": milestone.team.team_name}
                for milestone in recent_milestone_completions
                if milestone.team
            ]

            if not result:
                return (
                    jsonify(
                        {
                            "team": "No milestone completions in the last 7 days",
                        }
                    ),
                    200,
                )

            return jsonify(result), 200
        except Exception as e:
            return createFatalError(
                "milecomps_fetching_error",
                "Error fetching milestone completions",
                str(e),
            )


@api_bp_tahome.route("/api/submissions/uploads")
class UploadsResource(Resource):
    @jwt_required()
    @api_bp_tahome.response(200, UploadsResponse)
    def get(self):
        """Get teams who have uploaded documents in last 7 days"""
        try:
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
            recent_submissions = (
                db.session.query(Submission, Team.team_name)
                .join(Team, Submission.team_id == Team.team_id)
                .filter(Submission.submission_timestamp >= seven_days_ago)
                .all()
            )
            result = [
                {"team": team_name} for submission, team_name in recent_submissions
            ]

            if not result:
                return (
                    jsonify(
                        {
                            "team": "No uploads in the last 7 days",
                        }
                    ),
                    200,
                )

            return jsonify(result), 200
        except Exception as e:
            return createFatalError(
                "uploads_fetching_error", "Error fetching uploads", str(e)
            )
