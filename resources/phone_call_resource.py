from http import HTTPStatus
import os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import assemblyai as aai

from schemas.call_transcription_schema import (
    CallTranscriptionSchema,
    CallRecordingSchema,
)

phone_call_blueprint = Blueprint(
    "Phone Call Resource",
    __name__,
    description="Resource the phone call",
)


@phone_call_blueprint.route("/transcribe")
class CallTranscribing(MethodView):

    @phone_call_blueprint.response(HTTPStatus.OK, CallTranscriptionSchema)
    @phone_call_blueprint.arguments(CallRecordingSchema)
    def post(self, call_data):
        """Method to transcribe the call using assemblyAI"""
        try:
            aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(call_data["file_url"])
            return transcript, HTTPStatus.OK
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
