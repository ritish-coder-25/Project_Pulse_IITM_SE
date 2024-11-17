from flask import jsonify
from flask_jwt_extended import jwt_required
from models import db, Submission, Team
from flask_restx import Resource
from flask_smorest import Blueprint
from api_outputs.submissions_api.TADuploads_api_outputs import UploadsResponse
from datetime import datetime, timedelta, timezone
from helpers.ErrorCommonHelpers import createError, createFatalError
from sqlalchemy.orm import aliased

api_bp_uploads = Blueprint(
    "Uploads-Api",
    "Uploads",
    description="Operation for getting uploads in last 7 days",
)


@api_bp_uploads.route("/api/submissions/uploads")
class UploadsResource(Resource):
    @jwt_required()
    @api_bp_uploads.response(200, UploadsResponse)
    def get(self):
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
                return jsonify({"message": "No uploads in the last 7 days"}), 200

            return jsonify({"uploads": result}), 200
        except Exception as e:
            return createFatalError(
                "uploads_fetching_error", "Error fetching uploads", str(e)
            )
