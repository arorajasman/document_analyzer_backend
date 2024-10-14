from flask import Flask
from flask_injector import FlaskInjector
from flask_socketio import SocketIO
from injector import Injector, singleton, Binder

from services.audio_streaming_service import AudioStreamingService
from services.transcribe_summary_service import TranscribeSummary
from services.vectorstore_service import VectorStoreService
from flask_app import socketio, app
from websockets_resources.websocket_server import WebSocketServer


def configure_dependency_container(binder: Binder):
    """Method to configure the dependency injection for the project"""

    # configuring the dependencies
    binder.bind(SocketIO, to=socketio, scope=singleton)
    binder.bind(WebSocketServer, to=WebSocketServer, scope=singleton)
    binder.bind(
        AudioStreamingService,
        to=AudioStreamingService,
        scope=singleton,
    )
    binder.bind(TranscribeSummary, to=TranscribeSummary, scope=singleton)


def get_injector_instance() -> FlaskInjector:
    """Method to get the injector instance"""

    flask_injector = FlaskInjector(
        app,
        injector=Injector(configure_dependency_container),
    )

    return flask_injector.injector


def get_app_config(app: Flask, database_service: VectorStoreService):
    """Method to get the config for the app"""

    app.config["API_TITLE"] = "Document Analyzer"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # noqa
    )

    # config to get access to database service
    app.config["vectorstore_service"] = database_service

    return app
