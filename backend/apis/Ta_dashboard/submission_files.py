
from flask import request, jsonify
import os
from flask_jwt_extended import jwt_required
from flask import send_file, abort
from models import db, User, Team
from flask_jwt_extended import get_jwt_identity
from api_parsers import team_parsers
from flask_restx import Resource
from flask_smorest import Blueprint
from models import Submission, File, Milestone
from api_outputs.api_outputs_common import TeamSchema, CommonErrorSchema, CommonErrorErrorSchemaFatal
from api_outputs.teams_api.teams_api_output import TeamsCreateOutput, TeamsDeleteOutput
from api_outputs.teams_api.submission_output import DocumentListSchema, FileDownloadSchema
from helpers.ErrorCommonHelpers import createError, createFatalError

api_bp_submission = Blueprint("Submissions", "Milestones", description="Operations on teams milestone submissions and scoring")

@api_bp_submission.route("/api/files/<int:team_id>", methods=["GET"])
class SubmissionFileResource(Resource):

    @jwt_required()
    @api_bp_submission.response(200, DocumentListSchema)  # Assuming you define a schema for response
    @api_bp_submission.response(404, CommonErrorSchema)
    def get(self):
        """
        Get all files submitted by a specific team.

        Query Parameters:
            - team_id (int): The ID of the team whose submissions are being queried.

        Returns:
            List of documents with their metadata.
        """
        try:
            team_id = request.args.get("team_id", type=int)
            if not team_id:
                return {"errorCode": "missing_team_id", "message": "Team ID is required."}, 400

            submissions = Submission.query.filter_by(team_id=team_id).all()
            if not submissions:
                return {"errorCode": "submissions_not_found", "message": "No submissions found for the specified team."}, 404

            documents = []
            for submission in submissions:
                # Fetch files for the submission
                files = File.query.filter_by(submission_id=submission.submission_id).all()
                team = Team.query.get(submission.team_id)
                milestone = Milestone.query.get(submission.milestone_id)

                for file in files:
                    document = {
                        "id": file.file_id,
                        "name": file.file_name,
                        "url": f"http://localhost:5000/api/download/{file.file_id}",
                        "team": team.team_name,
                        "milestone": milestone.milestone_name,
                    }
                    documents.append(document)

            return {"documents": documents}, 200
        except Exception as e:
            return {"errorCode": "error", "message": "An error occurred.", "error": str(e)}, 500



@api_bp_submission.route("/api/download/<int:file_id>", methods=["GET"])
class FileDownloadResource(Resource):

    @jwt_required()
    @api_bp_submission.response(200, FileDownloadSchema)  # Assuming you define a schema for response
    @api_bp_submission.response(404, CommonErrorSchema)
    @api_bp_submission.response(500, CommonErrorSchema)
    def get(self, file_id):
        """
        Download a submitted file by its ID.

        Args:
            file_id (int): The ID of the file to download.

        Returns:
            The requested file as an attachment.

        Raises:
            - 404: If file not found in database or on server.
            - 500: If there is a server error.
        """
        try:
            file = File.query.get_or_404(file_id)
            file_path = os.path.join("file_submissions", file.file_name)

            if not os.path.exists(file_path):
                return {"errorCode": "file_not_found", "message": "File not found on server."}, 404

            return send_file(file_path, as_attachment=True, download_name=file.file_name)
        except Exception as e:
            return {"errorCode": "error", "message": "An error occurred.", "error": str(e)}, 500
############################
