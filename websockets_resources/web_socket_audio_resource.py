from flask_socketio import SocketIO
from injector import inject

from websockets_resources.websocket_resource import WebSocketResource


class WebSocketAudioResource(WebSocketResource):
    """Class to handle the audio processing using web sockets"""

    @inject
    def __init__(self, socketIO: SocketIO):
        self.socketIO = socketIO

        # registering audio_track event
        self.socketIO.on_event(
            "audio_track",
            namespace=self.signalling_server_namespace,
            handler=self.__handle_audio_track_event__,
        )

    def __handle_audio_track_event__(self, data):
        """Method to handle the audio track event"""
