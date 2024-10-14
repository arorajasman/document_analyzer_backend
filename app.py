from dotenv import load_dotenv
from flask_cors import CORS

from flask_app import app
from flask_smorest import Api

from resources.twilio_resource import twilio_blueprint
from resources.transcribe import bp as transcribe_bp
from resources.phone_call_resource import phone_call_blueprint
from resources.documents_resource import documents_blueprint

# from services.audio_streaming_service import AudioStreamingService
from utils.app_config import (
    get_app_config,
    get_injector_instance,
)  # noqa
from services.vectorstore_service import VectorStoreService
from websockets_resources.websocket_server import WebSocketServer

# loading .env file
load_dotenv()

# adding CORS
CORS(app)

# instannce of audio service
# audio_streaming_service = get_injector_instance().get(AudioStreamingService)

# database initialization
database_service = VectorStoreService()

# getting app config
config = get_app_config(app, database_service)

api = Api(app)
api.register_blueprint(twilio_blueprint)
api.register_blueprint(transcribe_bp)
api.register_blueprint(phone_call_blueprint)
api.register_blueprint(documents_blueprint)


web_socket_server: WebSocketServer = get_injector_instance().get(
    WebSocketServer
)  # noqa
