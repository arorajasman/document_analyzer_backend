from http import HTTPStatus

from flask import jsonify
from flask_app import app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from services.database_service import DatabaseService
from services.documents_service import DocumentsService
from utils.app_enums import DocType


documents_blueprint = Blueprint(
    "Documents Resource",
    __name__,
    description="Resource for working with documents",
    url_prefix="/documents",
)


@documents_blueprint.route("/create")
class CreateDocumentsResource(MethodView):
    """Resource to get the list of embeddings and save them to the database"""

    def post(self):
        try:
            # getting the documents
            document_service = DocumentsService()
            documents = document_service.load_documents(
                DocType.PDF,
                "PolicyDocs/ActiveStartPlan35G_MH000030_EOC.pdf",
                True,
            )
            # saving the documents
            database_service: DatabaseService = app.config["database_service"]
            database_service.store_documents_in_db(documents)

            # returning the documents to the user
            docs_list = []
            for document in documents:
                docs_list.append(
                    {
                        "page": document.page_content,
                        "meta_data": document.metadata,
                    }
                )

            return (
                jsonify({"count": len(docs_list), "documents": docs_list}),
                200,
            )

        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))


@documents_blueprint.route("/<string:document_key>")
class DocumentsResource(MethodView):
    """Resource to work with documents"""

    def get(self, document_key):
        """Method to get the documents list based on the key"""
        try:

            # getting the documents based on key from database
            database_service: DatabaseService = app.config["database_service"]
            documents = database_service.get_document_with_similarity(
                document_key
            )  # noqa

            # returning the documents to the user
            docs_list = []
            for document in documents:
                docs_list.append(
                    {
                        "page": document.page_content,
                        "meta_data": document.metadata,
                    }
                )

            return (
                jsonify({"count": len(docs_list), "documents": docs_list}),
                200,
            )

        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
