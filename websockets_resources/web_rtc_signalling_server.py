from flask import request
from flask_socketio import SocketIO, disconnect, emit, join_room
from injector import inject


class WebRTCSignallingServer:
    """Class to create the signalling server for the webRTC"""

    signalling_namespace = "/signalling-server"

    @inject
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

        # code to register connect event for connecting the user to the
        # signalling server
        socketio.on_event(
            "connect",
            namespace=self.signalling_namespace,
            handler=self.__handle_connection_event,
        )

        # code to register the event to make a new call
        socketio.on_event(
            "make_call",
            namespace=self.signalling_namespace,
            handler=self.__handle_make_call_event,
        )

        # code to register the answer_call event
        socketio.on_event(
            "answer_call",
            namespace=self.signalling_namespace,
            handler=self.__handle_answer_call_event,
        )

        # code to register the ice_candidate event
        socketio.on_event(
            "ice_candidate",
            namespace=self.signalling_namespace,
            handler=self.__handle_ice_candidate_event,
        )

    def __handle_connection_event(self, data):
        """Method to handle the connection event"""

        caller_id = request.args.get("callerId")
        if caller_id:
            # request.sid = caller_id  # attach callerId as user
            print(f"{caller_id} Connected")
            join_room(caller_id, namespace=self.signalling_namespace)

            emit(
                "user_connected",
                {
                    "id": caller_id,
                    "message": "User Connected",
                },  # noqa
                namespace=self.signalling_namespace,
            )
        else:
            # Disconnect if callerId is not present
            return disconnect()

    def __handle_make_call_event(self, data):
        """Method to handle the make call event"""

        callee_id = data.get("calleeId")
        sdp_offer = data.get("sdpOffer")

        print("make call event hit")
        if callee_id:

            print("emitting new call event")
            emit(
                "new_call",
                {"callerId": request.sid, "sdpOffer": sdp_offer},
                room=callee_id,
            )
        else:
            raise Exception("Id of Callee not found")

    def __handle_answer_call_event(self, data):
        """Method to handle the event to answer the call"""

        caller_id = data.get("callerId")
        sdp_answer = data.get("sdpAnswer")
        if caller_id:
            emit(
                "call_answered",
                {"callee": request.sid, "sdpAnswer": sdp_answer},
                room=caller_id,
            )

    def __handle_ice_candidate_event(self, data):
        """Method to handle the ice call event"""

        callee_id = data.get("calleeId")
        ice_candidate = data.get("iceCandidate")
        if callee_id:
            emit(
                "ice_candidate",
                {"sender": request.sid, "iceCandidate": ice_candidate},
                room=callee_id,
            )
