from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .config import CHROMA_DIR, EMBED_MODEL
from .loaders import get_splitter, load_document


class RAGEngine:
    """
    Core Lexora engine for document indexing.

    Phase 4 responsibilities:
    - Initialize the embedding model.
    - Initialize the persistent Chroma vector store.
    - Load documents.
    - Split documents into chunks.
    - Generate and store embeddings.
    """

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=self.embeddings,
        )

        self.splitter = get_splitter()

    def index_file(self, file_path: str | Path) -> dict:
        """
        Load, chunk, and index a supported document.
        """

        path = Path(file_path)

        documents = load_document(path)
        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata.update(
                {
                    "source": path.name,
                    "chunk_index": index,
                    "page": chunk.metadata.get("page", 0),
                }
            )

        self.vectorstore.add_documents(chunks)

        return {
            "ok": True,
            "source": path.name,
            "chunks": len(chunks),
        }

    def stats(self) -> dict:
        """Return basic information about the vector store."""

        data = self.vectorstore.get()

        return {
            "total_chunks": len(data["ids"]),
        }
