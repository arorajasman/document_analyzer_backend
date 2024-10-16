from flask import request
from flask_socketio import SocketIO, disconnect, emit, join_room
from injector import inject


class WebRTCSignallingServer:
    """Class to create the signalling server for the webRTC"""

    # property to get the namespace for the websocket
    __signalling_namespace__ = "/signalling-server"

    __socket_details__ = {}
    __room_id__ = ""
    __room_name__ = "Web_RTC_Room"

    @inject
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

        # code to register connect event for connecting the user to the
        # signalling server
        socketio.on_event(
            "connect",
            namespace=self.__signalling_namespace__,
            handler=self.__handle_connection_event,
        )

        # code to register the event to make a new call
        socketio.on_event(
            "make_call",
            namespace=self.__signalling_namespace__,
            handler=self.__handle_make_call_event,
        )

        # code to register the answer_call event
        socketio.on_event(
            "answer_call",
            namespace=self.__signalling_namespace__,
            handler=self.__handle_answer_call_event,
        )

        # code to register the ice_candidate event
        socketio.on_event(
            "ice_candidate",
            namespace=self.__signalling_namespace__,
            handler=self.__handle_ice_candidate_event,
        )

    def __handle_connection_event(self, data):
        """Method to handle the connection event"""

        caller_id = request.args.get("callerId")
        if caller_id and request.sid:
            self.__socket_details__[request.sid] = {
                "id": caller_id,
            }
            print(f"{caller_id} Connected to room with socket id {request.sid}")  # noqa
            join_room(
                self.__room_name__,
                sid=request.sid,
                namespace=self.__signalling_namespace__,
            )
        else:
            # Disconnect if callerId is not present
            return disconnect()

    def __handle_make_call_event(self, data):
        """Method to handle the make call event"""

        callee_id = data.get("calleeId")
        sdp_offer = data.get("sdpOffer")

        print("make call event hit")
        if callee_id and sdp_offer and request.sid:

            caller_id = self.__socket_details__[request.sid]["id"]
            if caller_id == "" or not caller_id:
                raise Exception("caller id not found")

            print("emitting new call event")
            print(
                {
                    "callerId": caller_id,
                    "sdpOffer": sdp_offer,
                    "callee_id": callee_id,
                },
            )
            print(f"Making a call from {caller_id} to {callee_id}")

            emit(
                "new_call",
                {"callerId": caller_id, "sdpOffer": sdp_offer},
                room=self.__room_name__,
            )
        else:
            raise Exception("Id of Callee not found")

    def __handle_answer_call_event(self, data):
        """Method to handle the event to answer the call"""

        caller_id = data.get("callerId")
        sdp_answer = data.get("sdpAnswer")
        if caller_id and sdp_answer:
            print(f"sdp answer: {sdp_answer}")
            emit(
                "call_answered",
                {"sdpAnswer": sdp_answer},
                room=self.__room_name__,
            )

    def __handle_ice_candidate_event(self, data):
        """Method to handle the ice call event"""

        callee_id = data.get("calleeId")
        ice_candidate = data.get("iceCandidate")
        if callee_id and ice_candidate:
            print(f"ice candidate: {ice_candidate}")
            emit(
                "ice_candidate",
                {"sender": callee_id, "iceCandidate": ice_candidate},
                room=self.__room_name__,
            )
