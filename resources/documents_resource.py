from http import HTTPStatus

from flask import jsonify
from flask_app import app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from services.vectorstore_service import VectorStoreService
from services.documents_service import DocumentsService
from utils.app_enums import DocType
from schemas.documents_schema import CreateDocument, GetDocumentSchema


documents_blueprint = Blueprint(
    "Documents Resource",
    __name__,
    description="Resource for working with documents",
    url_prefix="/documents",
)


@documents_blueprint.route("")
class CreateDocumentsResource(MethodView):
    """Resource to get the list of embeddings and save them to the database"""

    @documents_blueprint.arguments(CreateDocument)
    def post(self, document_data):
        """Create a new document in the vector database"""

        try:
            # getting the documents
            document_service = DocumentsService()
            errors = []
            for document_url in document_data["file_urls"]:
                try:
                    documents = document_service.load_documents(
                        DocType.PDF,
                        document_url,
                        True,
                    )
                    # saving the documents
                    vectorStoreService: VectorStoreService = app.config[
                        "vectorstore_service"
                    ]  # noqa
                    vectorStoreService.store_documents_in_db(documents)
                except Exception as e:
                    errors.append({"error": str(e), "file_url": document_url})
                    print(f"Error processing document: {e}")

            if errors:
                return jsonify({"errors": errors}), HTTPStatus.BAD_REQUEST

            return (
                jsonify({"message": "Documents created successfully"}),
                HTTPStatus.CREATED,
            )

        except Exception as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))

    @documents_blueprint.arguments(GetDocumentSchema, location="query")
    def get(self, query_args):
        """Method to get the documents list based on the key"""
        try:

            # getting the documents based on key from database
            vectorStoreService: VectorStoreService = app.config[
                "vectorstore_service"
            ]  # noqa
            documents = vectorStoreService.get_document_with_similarity(
                query_args["document_search_key"]
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
