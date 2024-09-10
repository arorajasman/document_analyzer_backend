from marshmallow import Schema, fields


class CallTranscriptionSchema(Schema):
    """Schema to return the details of the transcribed call"""

    id = fields.Str(allow_none=True)
    language_model = fields.Str(allow_none=True)
    acoustic_model = fields.Str(allow_none=True)
    language_code = fields.Str(allow_none=True)
    status = fields.Str(required=True)
    audio_url = fields.Str(allow_none=True)
    text = fields.Str(allow_none=True)
    words = fields.List(fields.Dict(), allow_none=True)
    utterances = fields.Raw(
        allow_none=True
    )  # since utterances is NULL, Raw can handle any type
    confidence = fields.Float(required=True)
    audio_duration = fields.Int(required=True)
    punctuate = fields.Bool(required=True)


class CallRecordingSchema(Schema):
    """Schema to get the file for transribing"""

    file_url = fields.Str(required=True)
