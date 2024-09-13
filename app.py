from dotenv import load_dotenv
from flask_cors import CORS
from flask_app import app
from flask_smorest import Api

from resources.twilio_resource import twilio_blueprint
from resources.transcribe import bp as transcribe_bp
from resources.phone_call_resource import phone_call_blueprint
from resources.documents_resource import documents_blueprint
from utils.app_config import get_app_config
from services.database_service import DatabaseService

# loading .env file
load_dotenv()

# adding CORS
CORS(app)


# database initialization
database_service = DatabaseService()

# getting app config
config = get_app_config(app, database_service)

api = Api(app)
api.register_blueprint(twilio_blueprint)
api.register_blueprint(transcribe_bp)
api.register_blueprint(phone_call_blueprint)
api.register_blueprint(documents_blueprint)
