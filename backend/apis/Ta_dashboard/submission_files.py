from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import os
from flask_jwt_extended import jwt_required
from flask import send_file, abort
from models import db, User, Team
from flask_jwt_extended import get_jwt_identity
from api_parsers import team_parsers
from flask_restx import Resource
from flask_smorest import Blueprint
from models import Submission, File, Milestone, MilestoneStatus
from api_outputs.api_outputs_common import (
    TeamSchema,
    CommonErrorSchema,
    CommonErrorErrorSchemaFatal,
    MilestoneReviewSchema,
    SpecificMilestoneStatus,
)
from api_outputs.teams_api.teams_api_output import TeamsCreateOutput, TeamsDeleteOutput
from api_outputs.teams_api.submission_output import (
    DocumentListSchema,
    FileDownloadSchema,
)
from helpers.ErrorCommonHelpers import createError, createFatalError

api_bp_submission = Blueprint(
    "Fetch Submissions APIs",
    "Fetch Submissions",
    description="Operations on teams milestone submissions and scoring",
)


@api_bp_submission.route("/api/files/<int:team_id>", methods=["GET"])
class SubmissionFileResource(Resource):

    @jwt_required()
    @api_bp_submission.response(
        200, DocumentListSchema
    )  # Assuming you define a schema for response
    @api_bp_submission.response(404, CommonErrorSchema)
    def get(self, team_id):
        """
        Get all files submitted by a specific team.

        Query Parameters:
            - team_id (int): The ID of the team whose submissions are being queried.

        Returns:
            List of documents with their metadata.
        """
        try:
            # team_id = request.args.get("team_id", type=int)
            # if not team_id:
            #     return {
            #         "errorCode": "missing_team_id",
            #         "message": "Team ID is required.",
            #     }, 400

            print("Team Id REceived: ", team_id)
            submissions = Submission.query.filter_by(team_id=team_id).all()
            if not submissions:
                return {
                    "errorCode": "submissions_not_found",
                    "message": "No submissions found for the specified team.",
                }, 404

            print(submissions)
            documents = []
            for submission in submissions:
                # Fetch files for the submission
                files = File.query.filter_by(
                    submission_id=submission.submission_id
                ).all()
                print(files)
                team = Team.query.get(submission.team_id)
                milestone = Milestone.query.get(submission.milestone_id)
                print(team)
                print(milestone)
                for file in files:
                    document = {
                        "id": file.file_id,
                        "name": file.file_name,
                        # "url": f"http://localhost:5000/api/download/{file.file_id}",
                        "team": team.team_name,
                        "milestone": milestone.milestone_name,
                    }
                    documents.append(document)
            print("Documents:",documents)
            return jsonify({"documents": documents}), 200 
        except Exception as e:
            return {
                "errorCode": "error",
                "message": "An error occurred.",
                "error": str(e),
            }, 500


@api_bp_submission.route("/api/download/<int:file_id>", methods=["GET"])
class FileDownloadResource(Resource):

    @jwt_required()
    @api_bp_submission.response(
        200, FileDownloadSchema
    )  # Assuming you define a schema for response
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
                return {
                    "errorCode": "file_not_found",
                    "message": "File not found on server.",
                }, 404

            return send_file(
                file_path, as_attachment=True, download_name=file.file_name
            )
        except Exception as e:
            return {
                "errorCode": "error",
                "message": "An error occurred.",
                "error": str(e),
            }, 500


@api_bp_submission.route("/api/milestone-review")
class MilestoneReviewSubmission(Resource):

    @api_bp_submission.response(
        200, MilestoneReviewSchema
    )  # Assuming you define a schema for response
    @api_bp_submission.response(404, CommonErrorSchema)
    @api_bp_submission.response(500, CommonErrorSchema)
    def post(self):
        """
        Create or update milestone review data.
        """
        try:
            data = request.json
            required_fields = [
                "team_id",
                "team_score",
                "milestone_id",
                "feedback",
                "max_milestone_score",
            ]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {
                    "errorCode": "missing_fields",
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                }, 400

            milestone_status = MilestoneStatus.query.filter_by(
                team_id=data["team_id"], milestone_id=data["milestone_id"]
            ).first()

            if milestone_status:
                # Update existing milestone review
                milestone_status.eval_score = data["team_score"]
                milestone_status.eval_feedback = data["feedback"]
                milestone_status.milestone_status = "Evaluated"
            else:
                # Create new milestone review
                milestone_status = MilestoneStatus(
                    team_id=data["team_id"],
                    milestone_id=data["milestone_id"],
                    milestone_status="Evaluated",
                    eval_score=data["team_score"],
                    eval_feedback=data["feedback"],
                )
                db.session.add(milestone_status)

            db.session.commit()
            return {"message": "Milestone review saved successfully."}, 201

        except SQLAlchemyError as db_err:
            db.session.rollback()
            return {
                "errorCode": "database_error",
                "message": "A database error occurred.",
                "error": str(db_err),
            }, 500
        except Exception as e:
            return {
                "errorCode": "unknown_error",
                "message": "An unexpected error occurred.",
                "error": str(e),
            }, 500

    def get(self):
        """
        Get all milestone reviews.
        """
        try:
            reviews = MilestoneStatus.query.all()
            return [review.to_dict() for review in reviews], 200
        except SQLAlchemyError as db_err:
            return {
                "errorCode": "database_error",
                "message": "A database error occurred.",
                "error": str(db_err),
            }, 500
        except Exception as e:
            return {
                "errorCode": "unknown_error",
                "message": "An unexpected error occurred.",
                "error": str(e),
            }, 500


@api_bp_submission.route("/api/milestone-review/<int:milestonestatus_id>")
class SpecificMilestoneReview(Resource):
    @api_bp_submission.response(
        200, SpecificMilestoneStatus
    )  # Assuming you define a schema for response
    @api_bp_submission.response(404, CommonErrorSchema)
    @api_bp_submission.response(500, CommonErrorSchema)
    def get(self, milestonestatus_id):
        """
        Get a specific milestone review by ID.
        """
        try:
            review = MilestoneStatus.query.get(milestonestatus_id)
            if not review:
                return {
                    "errorCode": "not_found",
                    "message": "Milestone review not found.",
                }, 404
            print("Data:",review.to_dict())
            return review.to_dict(), 200
        except SQLAlchemyError as db_err:
            return {
                "errorCode": "database_error",
                "message": "A database error occurred.",
                "error": str(db_err),
            }, 500
        except Exception as e:
            return {
                "errorCode": "unknown_error",
                "message": "An unexpected error occurred.",
                "error": str(e),
            }, 500

    def put(self, milestonestatus_id):
        """
        Update a specific milestone review by ID.
        """
        try:
            data = request.json
            review = MilestoneStatus.query.get(milestonestatus_id)
            if not review:
                return {
                    "errorCode": "not_found",
                    "message": "Milestone review not found.",
                }, 404

            # Update fields if they exist in the request
            review.eval_score = data.get("team_score", review.eval_score)
            review.eval_feedback = data.get("feedback", review.eval_feedback)
            review.milestone_status = data.get(
                "milestone_status", review.milestone_status
            )
            db.session.commit()

            return {"message": "Milestone review updated successfully."}, 200
        except SQLAlchemyError as db_err:
            db.session.rollback()
            return {
                "errorCode": "database_error",
                "message": "A database error occurred.",
                "error": str(db_err),
            }, 500
        except Exception as e:
            return {
                "errorCode": "unknown_error",
                "message": "An unexpected error occurred.",
                "error": str(e),
            }, 500

    def delete(self, milestonestatus_id):
        """
        Delete a specific milestone review by ID.
        """
        try:
            review = MilestoneStatus.query.get(milestonestatus_id)
            if not review:
                return {
                    "errorCode": "not_found",
                    "message": "Milestone review not found.",
                }, 404

            db.session.delete(review)
            db.session.commit()

            return {"message": "Milestone review deleted successfully."}, 200
        except SQLAlchemyError as db_err:
            db.session.rollback()
            return {
                "errorCode": "database_error",
                "message": "A database error occurred.",
                "error": str(db_err),
            }, 500
        except Exception as e:
            return {
                "errorCode": "unknown_error",
                "message": "An unexpected error occurred.",
                "error": str(e),
            }, 500
