from typing import Optional

import numpy as np
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from .config import RERANK_MODEL


class HybridRetriever:

    def __init__(self, vectorstore: Chroma):
        self.vectorstore = vectorstore
        self.reranker = CrossEncoder(RERANK_MODEL)
        self._bm25_index: Optional[BM25Okapi] = None
        self._bm25_docs: list[Document] = []
        self.rebuild_bm25()

    def rebuild_bm25(self):
        data = self.vectorstore.get()

        if not data["documents"]:
            self._bm25_index = None
            self._bm25_docs = []
            return

        self._bm25_docs = [
            Document(
                page_content=doc,
                metadata=meta,
            )
            for doc, meta in zip(
                data["documents"],
                data["metadatas"],
            )
        ]

        tokenized = [
            document.page_content.lower().split()
            for document in self._bm25_docs
        ]

        self._bm25_index = BM25Okapi(tokenized)

    def _bm25_search(
        self,
        query: str,
        k: int,
    ) -> list[Document]:

        if self._bm25_index is None:
            return []

        tokens = query.lower().split()
        scores = self._bm25_index.get_scores(tokens)

        top_k = np.argsort(scores)[::-1][:k]

        return [
            self._bm25_docs[index]
            for index in top_k
        ]

    def hybrid_search(
        self,
        query: str,
        k: int,
    ) -> list[Document]:

        indexed_count = len(self._bm25_docs)

        safe_k = (
            max(1, min(k, indexed_count))
            if indexed_count
            else 0
        )

        if safe_k == 0:
            return []

        vector_docs = self.vectorstore.similarity_search(
            query,
            k=safe_k,
        )

        bm25_docs = self._bm25_search(
            query,
            safe_k,
        )

        seen = set()
        merged = []

        for document in vector_docs + bm25_docs:
            key = document.page_content[:80]

            if key not in seen:
                seen.add(key)
                merged.append(document)

        return merged

    def rerank(
        self,
        query: str,
        docs: list[Document],
        top_n: int,
    ) -> list[tuple[Document, float]]:

        if not docs:
            return []

        pairs = [
            [query, document.page_content]
            for document in docs
        ]

        scores = self.reranker.predict(pairs)

        ranked = sorted(
            zip(docs, scores.tolist()),
            key=lambda item: item[1],
            reverse=True,
        )

        return ranked[:top_n]
