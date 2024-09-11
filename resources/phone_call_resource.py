from http import HTTPStatus
import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
import assemblyai as aai
from openai import OpenAI

from schemas.call_transcription_schema import (
    CallTranscriptionSchema,
    CallRecordingSchema,
)
from schemas.recording_summary_schema import (
    RecordingSummarySchema,
    Summary,
)
from utils.app_constants import app_strings
from services import faster_whisper_transcription


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
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(call_data["file_url"])
            return transcript, HTTPStatus.OK
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))


@phone_call_blueprint.route("/summary")
class CallSummary(MethodView):
    """Resource to get the summary of the recording"""

    @phone_call_blueprint.arguments(RecordingSummarySchema)
    @phone_call_blueprint.response(HTTPStatus.OK, Summary)
    def post(self, prompt_data):
        """Method to get the summary from the recording"""


        try:
            transcribed_data = faster_whisper_transcription.generate_transcription() 

            client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
            response_data = client.chat.completions.create(
                model="gpt-3.5-turbo",
                stream=False,
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": app_strings["summarization"],
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": prompt_data["prompt_text"],
                    },
                ],
            )

            return response_data.choices[0].message.content, HTTPStatus.OK
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
