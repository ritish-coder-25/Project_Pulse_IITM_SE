
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
from utils.github_helpers import get_commits_with_changes_files
from api_parsers.commit_github_parsers import CommitQueryParamsSchema
from api_outputs.teams_api.commit_github_output import CommitsResponseSchema

api_bp_GenAI = Blueprint("Fetch Commits APIs", "Fetch Commits", description="Fetch commit informaiton from GitHub for scoring analysis")

@api_bp_GenAI.route("/api/commits-fetch/<int:team_id>", methods=["GET"])
class GetAllCommitsResource(Resource):
    @jwt_required()
    @api_bp_GenAI.response(200, CommitsResponseSchema )  # Assuming you define a schema for response
    @api_bp_GenAI.response(404, CommonErrorSchema)
    @api_bp_GenAI.response(500, CommonErrorSchema)

    def get(self, query: CommitQueryParamsSchema):
        """
        Get all commits with file changes in a specified time frame from Github(to be used Internally using Celery).

        Args:
            - since (str): Start datetime in ISO format.
            - until (str): End datetime in ISO format.
            - repo_owner (str): GitHub repository owner.
            - repo_name (str): GitHub repository name.

        Returns:
            JSON response containing commit details grouped by user.

        Example Response:
            {
                "users": {
                    "ishdeep": {
                        "total_commits": 6,
                        "commit_details": [...]
                    },
                    "Ritish Kumar Das": {...}
                }
            }
        """
        try:
            # Call the utility function to fetch commits
            output = get_commits_with_changes_files(
                since=query.since,
                until=query.until,
                repo_owner=query.repo_owner,
                repo_name=query.repo_name,
            )

            # Assuming `output` is already structured as per the given example
            if not output:
                return {
                    "errorCode": "no_commits_found",
                    "message": "No commits found for the specified criteria."
                }, 404

            return jsonify({"users": output}), 200

        except Exception as e:
            return {
                "errorCode": "error",
                "message": "An error occurred while fetching commits.",
                "error": str(e)
            }, 500



