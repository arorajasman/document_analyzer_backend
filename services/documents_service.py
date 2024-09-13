from utils.app_enums import DocType
from typing import List
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentsService:
    """Class to work with documents"""

    def load_documents(self, type: DocType, path: str, isLocal: bool):
        """Method to load the documents"""

        match type:
            case DocType.PDF:
                return self.load_pdf_docs(path, isLocal)
            case DocType.DOCX:
                pass
            case DocType.TXT:
                pass
            case _:
                raise ValueError("Invalid document type")

    def load_pdf_docs(self, path: str, isLocal: bool):
        """Method to load pdf documents"""

        if isLocal:
            # loading the pdf file
            return self.load_and_split_pdf_doc(path)
        else:
            pass

    def load_and_split_pdf_doc(self, path: str):
        """Method for loading a single file"""

        loader = PyPDFLoader(path)

        # text splitter for splitting text
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        pages: List[Document] = loader.load_and_split(text_splitter)

        # adding unique doc_id for each document
        for page in pages:
            page.metadata["doc_id"] = str(uuid.uuid4())

        return pages
