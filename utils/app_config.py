from flask import Flask

from services.database_service import DatabaseService


def get_app_config(app: Flask, database_service: DatabaseService):
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
    app.config["database_service"] = database_service

    return app
