from http import HTTPStatus
import os

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import assemblyai as aai

from schemas.call_transcription_schema import (
    CallTranscriptionSchema,
    CallRecordingSchema,
    PolicyRankingSchema,
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
    def post(self, prompt_data):
        """Method to get the summary from the recording"""

        try:
            """################### FOR TESTING PURPOSE ###########"""
            file_url = prompt_data["file_url"]
            if not file_url:
                file_url = "assets/audio_files/policy_conv.mp3"
            """####################################################"""
            transcription_data: dict = TranscribeSummary.generate_transcription(  # noqa
                file_url,
            )  # noqa
            if "error" in transcription_data.keys():
                return abort(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    message=str(transcription_data["error"]),
                )
            # summary = TranscribeSummary.generate_summary(
            #     transcription_data["transcript"]
            # )  # noqa

            (summarization_response) = TranscribeSummary.generate_summary_v2(
                transcription_data["transcript"]
            )  # noqa  # noqa

            # keywords = TranscribeSummary.generate_keywords(summary)

            return (
                jsonify(
                    {
                        "recording_summary": summarization_response,
                    }
                ),
                HTTPStatus.OK,
            )
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))


@phone_call_blueprint.route("/generate_policies")
class PolicyRanking(MethodView):
    """Resource to get the policy ranking based on call summary"""

    @phone_call_blueprint.arguments(PolicyRankingSchema)
    def post(self, prompt_data):
        """Method to get the policy ranking based on call summary"""

        try:
            summary = prompt_data["summary"]

            (ranking_response) = TranscribeSummary.generate_policy_ranking(
                summary
            )  # noqa

            return (
                jsonify(
                    {"ranked_policies": ranking_response["policy_rankings"]}
                ),  # noqa
                HTTPStatus.OK,
            )
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))


@phone_call_blueprint.route("/generate_policies_agent")
class PolicyRankingAgent(MethodView):
    """Resource to get the policy ranking based on call summary using langchain agent"""  # noqa

    @phone_call_blueprint.arguments(PolicyRankingSchema)
    def post(self, prompt_data):
        """Method to get the policy ranking based on call summary using langchain agent"""  # noqa

        try:
            summary = prompt_data["summary"]

            (agent_response) = TranscribeSummary.generate_policy_agent(summary)  # noqa

            return (
                jsonify({"ranked_policies": agent_response}),
                HTTPStatus.OK,
            )
        except Exception as e:
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
