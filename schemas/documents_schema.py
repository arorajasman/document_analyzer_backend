from marshmallow import Schema, fields


class CreateDocument(Schema):
    """Schema to get the details to create document in the database"""

    file_urls = fields.List(fields.Str(), required=True)


class GetDocumentSchema(Schema):
    """Schema to get the list of documents based on key"""

    document_search_key = fields.Str()
