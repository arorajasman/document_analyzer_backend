from dotenv import load_dotenv
from flask_cors import CORS
from flask_app import app
from flask_smorest import Api

from resources.twilio_resource import twilio_blueprint
from resources.phone_call_resource import phone_call_blueprint

# loading .env file
load_dotenv()

# adding CORS
CORS(app)

app.config["API_TITLE"] = "Document Analyzer"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # noqa
)

api = Api(app)
api.register_blueprint(twilio_blueprint)
api.register_blueprint(phone_call_blueprint)
