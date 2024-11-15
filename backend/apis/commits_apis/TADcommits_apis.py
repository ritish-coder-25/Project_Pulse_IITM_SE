from flask import jsonify
from flask_jwt_extended import jwt_required
from models import db, Commit
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

            recent_commits = Commit.query.filter(
                Commit.commit_timestamp >= seven_days_ago
            ).all()

            result = [
                {"team": commit.team.team_name}
                for commit in recent_commits
                if commit.user and commit.user.team
            ]

            if not result:
                return (
                    jsonify(
                        {"message": "No commits in the last 7 days", "commits": []}
                    ),
                    200,
                )

            return jsonify({"commits": result}), 200
        except Exception as e:
            return createFatalError(
                "commits_fetching_error", "Error fetching commits", str(e)
            )
