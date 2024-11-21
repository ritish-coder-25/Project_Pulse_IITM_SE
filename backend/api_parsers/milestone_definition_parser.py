# api_parsers/TADMilestone_Definition_parser.py
from marshmallow import Schema, fields, validate
from datetime import datetime


class MilestoneSchema(Schema):
    milestone_name = fields.Str(required=True, validate=validate.Length(min=1))
    milestone_description = fields.Str(required=True, validate=validate.Length(min=1))
    start_date = fields.Str(
        required=True, 
        validate=validate.Regexp(
            r"^\d{4}-\d{2}-\d{2}$", 
            error="Start date must be in the format YYYY-MM-DD"
        )
    )
    end_date = fields.Str(
        required=True, 
        validate=validate.Regexp(
            r"^\d{4}-\d{2}-\d{2}$", 
            error="End date must be in the format YYYY-MM-DD"
        )
    )
    max_marks = fields.Float(required=True, validate=validate.Range(min=0))
    project_id = fields.Int(required=True)

class MilestoneUpdateSchema(Schema):
    milestone_name = fields.Str(validate=validate.Length(min=1))
    milestone_description = fields.Str(validate=validate.Length(min=1))
    start_date = fields.Str(
        validate=validate.Regexp(
            r"^\d{4}-\d{2}-\d{2}$", 
            error="Start date must be in the format YYYY-MM-DD"
        )
    )
    end_date = fields.Str(
        validate=validate.Regexp(
            r"^\d{4}-\d{2}-\d{2}$", 
            error="End date must be in the format YYYY-MM-DD"
        )
    )
    max_marks = fields.Float(validate=validate.Range(min=0))
