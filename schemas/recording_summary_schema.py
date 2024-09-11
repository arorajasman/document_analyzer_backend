from marshmallow import Schema, fields


class RecordingSummarySchema(Schema):
    """Schema for recording summary."""

    prompt_text = fields.Str(required=True)


class Summary(Schema):
    """Schema for summary."""

    recording_summary = fields.Str()
