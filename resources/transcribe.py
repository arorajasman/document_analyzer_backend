from flask import Response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from services import transcribe
from services import faster_whisper_transcription


bp = Blueprint(
    "Transcription",
    __name__,
    description="Transcription API",
)


@bp.route("/transcribe/faster_whisper")
class Transcribe(MethodView):

    def get(self):

        transcribed_data = faster_whisper_transcription.generate_transcription()

        print(transcribed_data)

        return jsonify(transcribed_data)
