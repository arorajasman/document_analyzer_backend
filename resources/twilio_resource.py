import os
from flask import Response, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client

from schemas.twilio_schema import CallUser


twilio_blueprint = Blueprint(
    "Twilio Resource",
    __name__,
    description="Resource for Twilio",
)


@twilio_blueprint.route("/twiml-file")
class Twilio(MethodView):

    def get(self):
        # Create a Twilio VoiceResponse object to generate TwiML
        response = VoiceResponse()

        # Add a message to be said in the call
        response.say("Hello, this is a Twilio call!")

        # Optional: Add more TwiML instructions
        response.pause(length=2)

        # Add a message to be said before connecting the call
        response.say("Connecting your call.")

        # Dial the number and set the recording option
        dial = Dial(record="record-from-ringing", time_limit=600)
        dial.number(os.getenv("DIAL_NUMBER"))  # The number you want to dial

        # Add the Dial to the response
        response.append(dial)

        response.say("Thank you for using our service. Goodbye!")

        # Return the TwiML as an XML response
        return Response(str(response), mimetype="text/xml")


@twilio_blueprint.route("/twilio-call")
class TwilioCallService(MethodView):

    @twilio_blueprint.arguments(CallUser)
    def post(self, data):
        # Retrieve the account SID and auth token from environment variables
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            return jsonify({"error": "Twilio credentials not found."}), 500

        # Initialize the Twilio client
        client = Client(account_sid, auth_token)

        # Get 'to' and 'from' phone numbers from the POST request body
        data = request.get_json()
        to_number = data["to_number"]

        if not to_number:
            return (
                jsonify({"error": "Missing 'to' phone numbers."}),
                400,
            )  # noqa

        try:
            # Make the call using the Twilio REST API
            call = client.calls.create(
                # TwiML URL for call instructions
                url="https://1ff6-103-212-131-81.ngrok-free.app/twiml-file",
                to=to_number,
                from_=os.getenv("DIAL_NUMBER"),
                record=True,
                time_limit=600,
            )

            print("Call data")
            print(call.__dict__)

            # Return a successful response with the call SID
            return (
                jsonify(
                    {
                        "message": "Call initiated successfully",
                        "call_sid": call.sid,
                    }
                ),
                200,
            )

        except Exception as e:

            print("error")
            print(e)
            # Handle any errors and return an appropriate response
            return jsonify({"error": str(e)}), 500
