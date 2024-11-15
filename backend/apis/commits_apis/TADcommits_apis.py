from flask import jsonify
from flask_jwt_extended import jwt_required
from models import db, Commit, Team, User
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.commits_api.TADcommits_api_outputs import CommitsResponse
from datetime import datetime, timedelta, timezone
from helpers.ErrorCommonHelpers import createError, createFatalError

api_bp_commits = Blueprint(
    "Commits-Api", "Commits", description="Operation for getting commits in last 7 days"
)


@api_bp_commits.route("/api/commits")
class CommitsResource(Resource):
    @jwt_required()
    @api_bp_commits.response(200, CommitsResponse)
    def get(self):
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
                    jsonify({"message": "No commits in the last 7 days"}),
                    200,
                )

            return jsonify({"commits": result}), 200
        except Exception as e:
            return createFatalError(
                "commits_fetching_error", "Error fetching commits", str(e)
            )
