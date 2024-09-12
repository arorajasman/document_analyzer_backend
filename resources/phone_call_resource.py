from http import HTTPStatus
import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
import assemblyai as aai

from schemas.call_transcription_schema import (
    CallTranscriptionSchema,
    CallRecordingSchema,
)
from schemas.recording_summary_schema import (
    Summary,
)
from services.transcribe_summary_service import TranscribeSummary


phone_call_blueprint = Blueprint(
    "Phone Call Resource",
    __name__,
    description="Resource the phone call",
    url_prefix="/phone-call",
)


@phone_call_blueprint.route("/transcribe")
class CallTranscribing(MethodView):

    @phone_call_blueprint.response(HTTPStatus.OK, CallTranscriptionSchema)
    @phone_call_blueprint.arguments(CallRecordingSchema)
    def post(self, call_data):
        """Method to transcribe the call using assemblyAI"""
        try:
            aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")
            config = aai.TranscriptionConfig(speaker_labels=True)
            transcriber = aai.Transcriber()
            transcript = (
                transcriber.transcribe(
                    call_data["file_url"],
                    config=config,
                ),
            )
            return transcript, HTTPStatus.OK
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))


@phone_call_blueprint.route("/summary")
class CallSummary(MethodView):
    """Resource to get the summary of the recording"""

    @phone_call_blueprint.arguments(CallRecordingSchema)
    @phone_call_blueprint.response(HTTPStatus.OK, Summary)
    def post(self, prompt_data):
        """Method to get the summary from the recording"""

        try:
            """################### FOR TESTING PURPOSE ###########"""
            file_url = prompt_data["file_url"]
            if not file_url:
                file_url = "audio_files/policy_conv.mp3"
            """####################################################"""
            transcription_data: dict = TranscribeSummary.generate_transcription(  # noqa
                file_url,
            )  # noqa
            if "error" in transcription_data.keys():
                return abort(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    message=str(transcription_data["error"]),
                )
            summary = TranscribeSummary.generate_summary(
                transcription_data["transcript"]
            )  # noqa
            return {"recording_summary": summary}, HTTPStatus.OK
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
