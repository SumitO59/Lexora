import json
from pathlib import Path
from typing import Optional

import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

from .analysis import analyze_document
from .config import CHROMA_DIR, EMBED_MODEL, META_PATH, OLLAMA_MODEL
from .loaders import get_splitter, load_document
from .retrieval import HybridRetriever
from .utils import file_hash

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a private document analyst. Use ONLY the context below to answer.
If the answer is not in the context, say "Not found in the uploaded documents."

Context:
{context}

Question: {question}

Answer:"""
)


class RAGEngine:
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
        self.retriever = HybridRetriever(self.vectorstore)
        self._llm: Optional[OllamaLLM] = None
        self._meta: dict = self._load_meta()

    def _get_llm(self, model: str = OLLAMA_MODEL) -> OllamaLLM:
        if self._llm is None or self._llm.model != model:
            self._llm = OllamaLLM(model=model, temperature=0.1)
        return self._llm

    def _load_meta(self) -> dict:
        if META_PATH.exists():
            return json.loads(META_PATH.read_text())
        return {}

    def _save_meta(self):
        META_PATH.write_text(json.dumps(self._meta, indent=2))

    def index_file(self, file_path: str, original_name: str = None, model: str = OLLAMA_MODEL) -> dict:
        path = Path(file_path)
        display_name = original_name or path.name

        docs = load_document(path)
        chunks = self.splitter.split_documents(docs)

        h = file_hash(path)
        for i, c in enumerate(chunks):
            c.metadata.update({
                "source": display_name,
                "file_hash": h,
                "chunk_index": i,
                "page": c.metadata.get("page", 0),
            })

        self._delete_file(display_name)
        self.vectorstore.add_documents(chunks)
        self.retriever.rebuild_bm25()

        full_text = "\n".join(d.page_content for d in docs)
        analysis = analyze_document(self._get_llm(model), full_text)

        self._meta[display_name] = {
            "chunks": len(chunks),
            "hash": h,
            **analysis,
        }
        self._save_meta()

        return {
            "ok": True,
            "msg": f"Indexed {len(chunks)} chunks from {display_name}",
            "analysis": analysis,
        }

    def _delete_file(self, filename: str):
        try:
            ids = self.vectorstore.get(where={"source": filename})["ids"]
            if ids:
                self.vectorstore.delete(ids=ids)
        except Exception:
            pass

    def delete_file(self, filename: str) -> dict:
        self._delete_file(filename)
        self._meta.pop(filename, None)
        self._save_meta()
        self.retriever.rebuild_bm25()
        return {"ok": True, "msg": f"Removed {filename} from index"}

    def query(self, question: str, model: str = OLLAMA_MODEL, k: int = 4) -> dict:
        llm = self._get_llm(model)
        pool = self.retriever.hybrid_search(question, k=k * 3)
        ranked = self.retriever.rerank(question, pool, top_n=k)

        context_parts = []
        citations = []

        for doc, score in ranked:
            context_parts.append(doc.page_content)
            norm_score = round(float(1 / (1 + np.exp(-score / 3))), 3)
            citations.append({
                "source": doc.metadata.get("source", "?"),
                "page": doc.metadata.get("page", None),
                "chunk": doc.metadata.get("chunk_index", "?"),
                "score": norm_score,
                "passage": doc.page_content[:250].strip(),
            })

        context = "\n\n---\n\n".join(context_parts)
        prompt = QA_PROMPT.format(context=context, question=question)
        answer = llm.invoke(prompt).strip()
        sources = list({c["source"] for c in citations})

        return {
            "answer": answer,
            "sources": sources,
            "citations": citations,
        }

    def stats(self) -> dict:
        data = self.vectorstore.get()
        files = list({m.get("source", "?") for m in data["metadatas"]}) if data["metadatas"] else []
        return {"total_chunks": len(data["ids"]), "files": files}

    def get_doc_meta(self, filename: str) -> Optional[dict]:
        return self._meta.get(filename)

    def all_meta(self) -> dict:
        return self._meta