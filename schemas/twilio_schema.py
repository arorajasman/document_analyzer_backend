from marshmallow import Schema, fields


class CallUser(Schema):
    """Schema for call user."""

    to_number = fields.Str()
