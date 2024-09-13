from flask_smorest import Blueprint


phone_call_blueprint = Blueprint(
    "Phone Call Resource",
    __name__,
    description="Resource the phone call",
    url_prefix="/phone-call",
)

