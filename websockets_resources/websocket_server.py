from flask_socketio import SocketIO, emit
from injector import inject


class WebSocketServer:

    @inject
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

        socketio.on_event(
            "offer",
            self.handle_offer,
        )

    def handle_offer(self, data):
        print("got the event hit")
        print(data)
        emit("offer_handler", data, broadcast=True)
