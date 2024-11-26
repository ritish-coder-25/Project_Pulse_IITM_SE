from flask import request, jsonify
import os, json
from flask_jwt_extended import jwt_required
from flask import send_file, abort
from datetime import datetime
from models import db, User, Team
from flask_jwt_extended import get_jwt_identity
from api_parsers import team_parsers
from flask_restx import Resource
from flask_smorest import Blueprint
from models import Submission, File, Milestone
from api_outputs.api_outputs_common import (
    TeamSchema,
    CommonErrorSchema,
    CommonErrorErrorSchemaFatal,
)
from api_outputs.teams_api.teams_api_output import TeamsCreateOutput, TeamsDeleteOutput
from api_outputs.teams_api.submission_output import (
    DocumentListSchema,
    FileDownloadSchema,
)
from helpers.ErrorCommonHelpers import createError, createFatalError
from utils.github_helpers import get_commits_with_changes_files
from utils.summarizer_chain import summarize_code_changes
from api_parsers.commit_github_parsers import CommitQueryParamsSchema
from api_outputs.teams_api.commit_github_output import CommitsResponseSchema

api_bp_GenAI = Blueprint(
    "Fetch Commits APIs",
    "Fetch Commits",
    description="Fetch commit informaiton from GitHub for scoring analysis",
)


@api_bp_GenAI.route("/api/commits-fetch", methods=["POST"])
class GetAllCommitsResource(Resource):
    @jwt_required()
    @api_bp_GenAI.response(
        200, CommitsResponseSchema
    )  # Assuming you define a schema for response
    @api_bp_GenAI.response(404, CommonErrorSchema)
    @api_bp_GenAI.response(500, CommonErrorErrorSchemaFatal)
    def post(self, ):
        """
        Get all commits with file changes in a specified time frame from Github(to be used Internally using Celery).

        Args:
            - team_id (int): The ID of the team.
            - query (CommitQueryParamsSchema): The query parameters.

        Returns:
            JSON response containing commit details grouped by user.

        Example Request Body:
            {
                "since": "2022-01-01T00:00:00",
                "until": "2022-01-31T23:59:59",
                "repo_owner": "ritish-coder-25",
                "repo_name": "Project_Pulse_IITM_SE",
                "team_id": 1
            }


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
            print("Received data", request.json)
            query = CommitQueryParamsSchema().load(request.json)
            print("Query: ", query)

            
            
            # if query["team_id"]:
            #     team = Team.query.get(query["team_id"])
            #     if not team:
            #         # return createError("Team not found.", 404)
            #         # return createError("404", "Team not found.")
            #         return createError(errorCode= "Since must be before after date.",message= "Team Not found", errorStatus= 400)
            
            # if query["since"] > query["until"]:
            #     # return createError("Invalid date range.", 400)
            #     return createError(errorCode= "Since must be before after date.",message= "Invalid Date Range", errorStatus= 400)
            
            if query["repo_owner"] is None or query["repo_name"] is None:
                output = get_commits_with_changes_files(
                    since=query["since"],
                    until=query["until"],
                    repo_name=None,
                    repo_owner=None,
                    # repo_url = team.to_dict()['github_repo_url']
                )
            

            else:
                output = get_commits_with_changes_files(
                since=query["since"],
                until=query["until"],
                repo_owner=query["repo_owner"],
                repo_name=query["repo_name"],
                
                )

            # Assuming `output` is already structured as per the given example
            if not output:
                return {
                    "errorCode": "no_commits_found",
                    "message": "No commits found for the specified criteria.",
                }, 404

            return jsonify({"users": output}), 200

        except Exception as e:
            return {
                "errorCode": "error",
                "message": "An error occurred while fetching commits.",
                "error": str(e),
            }, 500
        # Get all commits with file changes in a specified time frame from Github(to be used Internally using Celery).

        # Args:
        #     - since (str): Start datetime in ISO format.
        #     - until (str): End datetime in ISO format.
        #     - repo_owner (str): GitHub repository owner.
        #     - repo_name (str): GitHub repository name.

        # Returns:
        #     JSON response containing commit details grouped by user.

        # Example Response:
        #     {
        #         "users": {
        #             "ishdeep": {
        #                 "total_commits": 6,
        #                 "commit_details": [...]
        #             },
        #             "Ritish Kumar Das": {...}
        #         }
        #     }
        # """
        # try:
        #     # Call the utility function to fetch commits
        #     output = get_commits_with_changes_files(
        #         since=query.since,
        #         until=query.until,
        #         repo_owner=query.repo_owner,
        #         repo_name=query.repo_name,
        #     )

        #     # Assuming `output` is already structured as per the given example
        #     if not output:
        #         return {
        #             "errorCode": "no_commits_found",
        #             "message": "No commits found for the specified criteria.",
        #         }, 404

        #     return jsonify({"users": output}), 200

        # except Exception as e:
        #     return {
        #         "errorCode": "error",
        #         "message": "An error occurred while fetching commits.",
        #         "error": str(e),
        #     }, 500


@api_bp_GenAI.route("/api/genai-commits-analysis/<int:team_id>", methods=["POST"])
class GenAICommitAnalaysis(Resource):
    @jwt_required()
    def post(self, team_id):
        """
        Process and summarize code changes from a JSON file for a specific team.

        Args:
            - team_id (str): Identifier for the team/project.

        Body:
            {
                "file_path": "path_to_json_file"
            }

        Returns:
            JSON response with the summarized results.

        Example Response:
            {
                "summary": {
                    "Marmik Thaker": {
                        "commit_details": [...]
                    }
                }
            }
        """
        try:
            # Extract file path from request body and convert to absolute path
            data = request.json
            file_path = os.path.abspath(data.get("file_path"))  # Updated to use absolute path

            if not file_path or not os.path.exists(file_path):
                return {
                    "errorCode": "file_not_found",
                    "message": "The specified file does not exist.",
                }, 404

            # Read the JSON file
            with open(file_path, "r") as file:
                changes_all = json.load(file)

            if not changes_all:
                return {
                    "errorCode": "empty_file",
                    "message": "The file is empty or invalid.",
                }, 400

            # Example processing: limit changes to the first user's first commit details
            user_changes = changes_all[list(changes_all.keys())[0]]
            commit_details = user_changes["commit_details"]
            file_changes = commit_details[0]["file_changes"]
            code_changes = file_changes[0]["code_changes"]

            # Clean and summarize the code changes
            def clean_code(code):
                cleaned_code = code.strip()
                cleaned_code = " ".join(cleaned_code.split())
                return cleaned_code

            code_changes = clean_code(code_changes)
            if len(code_changes) > 1000:
                code_changes = code_changes[
                    :1000
                ]  # Limit to 1000 characters for testing

            summary = summarize_code_changes(code_changes)

            # Save summary to a file
            output_file = f"reports/{team_id}_{datetime.now().strftime('%Y-%m-%d_%H')}_summary.json"
            with open(output_file, "w") as file:
                file.write(json.dumps(summary, indent=4))

            # Return summary as response
            return jsonify({"summary": summary, "saved_to": output_file}), 200

        except Exception as e:
            return {
                "errorCode": "processing_error",
                "message": "An error occurred while processing and summarizing code changes.",
                "error": str(e),
            }, 500
