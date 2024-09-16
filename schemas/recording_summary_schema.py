from marshmallow import Schema, fields


class RecordingSummarySchema(Schema):
    """Schema for recording summary."""

    user_prompt = fields.Str(required=True)


class RankedPolicySchema(Schema):
    ranking = fields.Str()
    policy_name = fields.Str()
    document_source = fields.Str()


class Summary(Schema):
    """Schema for summary."""

    recording_summary = fields.Str()
    ranked_policies = fields.List(fields.Nested(RankedPolicySchema))
