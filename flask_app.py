from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

# socket IO config for working with web sockets
socketio = SocketIO(
    app,
    debug=True,
    cors_allowed_origins="*",
)
