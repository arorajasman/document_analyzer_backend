from flask_socketio import SocketIO, emit
from injector import inject

from services.transcribe_summary_service import TranscribeSummary


class AudioStreamingService:
    """Service to work with audio streaming"""

    @inject
    def __init__(self, socketio: SocketIO, summary: TranscribeSummary):
        self.socketIO = socketio
        self.summary = summary

        # registering the event for trancribe_audio
        socketio.on_event(
            "transcribe_audio",
            handler=self.stream_audio_transcription,
        )

    def stream_audio_transcription(self, data):
        """
        Method to stream audio transcription to the user

        Attributes
        ----------
        data : dict
            - Data recieved from the client
        """

        print(f"[AudioStreamingService]: service hit with data {data}")

        # summary = self.summary.get_transcription_with_assembly_ai(data)

        emit("summary_data", {"summary": "summary success"})
