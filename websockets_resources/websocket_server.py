from flask_socketio import SocketIO, emit
from injector import inject


class WebSocketServer:

    @inject
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

        socketio.on_event(
            "offer",
            handler=self.handle_offer,
        )

    def run(self, host="0.0.0.0", port=5000, debug=True):
        self.socketio.run(
            app=self.socketio.server,
            host=host,
            port=port,
            debug=debug,
        )

    def handle_offer(data):
        print("got the event hit")
        print(data)
        emit("offer_handler", data, broadcast=True)
