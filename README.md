# Lexora

Lexora is a local-first AI document analyst that lets you upload documents, index them locally, and ask natural-language questions over their contents.

It combines semantic retrieval, keyword retrieval, cross-encoder reranking, and a local Ollama language model to produce grounded answers with source citations. It also automatically extracts document summaries, named entities, and important numerical information.

The entire workflow is designed to run locally, keeping uploaded documents and generated indexes on your machine.

## Features

### Local RAG Pipeline

Lexora uses a multi-stage retrieval pipeline instead of relying on simple keyword matching:

Documents are loaded and split into chunks.
Chunks are embedded using BAAI/bge-small-en-v1.5.
Semantic retrieval is performed using ChromaDB.
BM25 provides lexical retrieval.
Results from both retrieval methods are merged.
A cross-encoder reranks the retrieved passages.
Ollama generates the final grounded answer.
This hybrid retrieval + reranking architecture improves retrieval quality while keeping the entire pipeline local.

### Natural-Language Document Q&A

Ask questions such as:

What are the main findings of this report?

What revenue growth is mentioned?

Who are the organizations referenced in the document?

What are the key risks discussed?

Summarize the methodology used in this paper.
Lexora uses only retrieved document context when generating answers. When the information is not available in the indexed material, the system is instructed to say:

Not found in the uploaded documents.

### Multi-Format Document Support

The application supports:

PDF
DOCX
TXT
Markdown
XLSX
Each uploaded document is processed and indexed locally.

### Hybrid Search

Lexora combines:

Vector similarity search
BM25 keyword search
Cross-encoder reranking
The semantic retriever captures conceptual similarity, while BM25 helps preserve exact keyword matches. The combined candidates are then reranked before being passed to the language model.

### Source Citations

Answers are accompanied by source information including:

Document name
Page number when available
Chunk index
Retrieval confidence
Source passage
This provides traceability between generated answers and the underlying documents.

### Automatic Document Insights

When a document is uploaded, Lexora automatically generates:

A concise document summary
Named entities
People
Organizations
Locations
Dates
Important numbers
Statistics
Percentages
Monetary values
These insights are available through the Document Insights tab.

### Document Management

The sidebar provides:

Indexed document list
Chunk counts
Individual document deletion
Chat history clearing
Re-uploading the same document replaces its previous indexed representation.

### Local Generative AI

Lexora uses Generative AI through a locally running Ollama language model.

The default model is:

```text
llama3
```

The local LLM is used for:

- Grounded question answering
- Document summarization
- Named-entity extraction
- Important-number extraction

No external AI API is required for the core GenAI workflow.

### Privacy-First Architecture

Lexora is designed as a local RAG system.

Document processing, embeddings, retrieval, reranking, and LLM generation are intended to run locally through:

Hugging Face embedding models
ChromaDB
Sentence Transformers
Ollama
No external API is required for the core question-answering workflow.

## Architecture

```
                    ┌─────────────────────┐
                    │    Document Upload  │
                    │ PDF/DOCX/TXT/MD/XLSX│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Document Loading    │
                    │ Format-specific     │
                    │ Parsers             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Text Chunking       │
                    │ 512 characters      │
                    │ 64 overlap          │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Vector Search    │        │ BM25 Search      │
       │ ChromaDB         │        │ Keyword Retrieval│
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ Candidate Merging   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Cross-Encoder       │
                    │ Reranking           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Ollama Local LLM    │
                    │ Grounded Generation │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Citations  │
                    └─────────────────────┘
```

The current implementation uses BAAI/bge-small-en-v1.5 for embeddings, cross-encoder/ms-marco-MiniLM-L-6-v2 for reranking, ChromaDB for persistent vector retrieval, BM25 for lexical retrieval, and Ollama for local generation.

## Project Structure

```
Lexora/
│
├── app.py                 # Streamlit frontend
├── requirements.txt
├── README.md
├── .gitignore
│
└── src/
    ├── __init__.py         # exposes RAGEngine, OLLAMA_MODEL
    ├── config.py            # paths, model names, chunking constants
    ├── loaders.py           # per-format document loading + text splitter
    ├── retrieval.py          # HybridRetriever: vector + BM25 + reranking
    ├── analysis.py           # LLM-based summary / entity / number extraction
    ├── utils.py              # file hashing, JSON extraction from LLM output
    └── engine.py             # RAGEngine — orchestrates the pipeline
```

### app.py

The Streamlit frontend provides:

Document upload
Local model selection
Retrieval depth control
Chat interface
Source citations
Document insights
Indexed file management
The current UI is configured as a wide Streamlit application with an expanded sidebar.

### src/

The core RAG implementation, split by responsibility:

loaders.py — document loading and chunking
retrieval.py — hybrid search (vector + BM25) and cross-encoder reranking
analysis.py — document summaries, entity extraction, key-number extraction
utils.py — file hashing and JSON extraction helpers
engine.py — RAGEngine, which ties the above together for indexing, querying, and deletion

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| RAG framework | LangChain |
| Embeddings | Hugging Face / BAAI/bge-small-en-v1.5 |
| Vector store | ChromaDB |
| Keyword retrieval | BM25 |
| Reranking | ms-marco-MiniLM-L-6-v2 |
| Generative AI | Ollama / Llama 3 |
| Document parsing | PyPDF / python-docx / openpyxl |
| Numerical processing | NumPy |
| Language | Python |

## Installation

### 1. Clone the repository

```
git clone https://github.com/SumitO59/Lexora.git
cd Lexora
```

### 2. Create a virtual environment

**Windows**
```
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

The repository's dependency configuration includes Streamlit, LangChain-related packages, ChromaDB, Hugging Face embeddings, Sentence Transformers, BM25 retrieval, and Ollama integration.

### 4. Install Ollama

Install Ollama locally and make sure it is available from your terminal.

Then pull a supported model, for example:

```
ollama pull llama3
```

Other model choices exposed by the application include:

llama3
mistral
phi3
gemma2

## Running the Application

Start the Streamlit application with:

```
streamlit run app.py
```

The browser-based interface provides two main views:

**Chat**
Ask questions over your indexed documents and inspect the generated answer and supporting citations.

**Document Insights**
View automatically generated:

Summaries
Named entities
Important numbers
Chunk counts

## Retrieval Pipeline

Lexora uses a hybrid retrieval strategy.

### 1. Semantic Retrieval

Documents are embedded using:

BAAI/bge-small-en-v1.5
The resulting vectors are stored in ChromaDB for similarity search.

### 2. BM25 Retrieval

A BM25 index is constructed over the indexed chunks to capture lexical matches and exact terminology.

### 3. Candidate Fusion

Semantic and BM25 results are merged while removing duplicate passages.

### 4. Reranking

The merged candidates are passed through:

cross-encoder/ms-marco-MiniLM-L-6-v2
The reranker scores query-passage pairs and selects the strongest candidates.

### 5. Grounded Generation

The top passages are inserted into a constrained prompt and passed to the selected Ollama model.

The model is explicitly instructed to answer only from the retrieved context.

## Document Analysis

Lexora performs additional analysis during indexing.

### Summary

The document is summarized into 3–5 concise sentences.

### Entity Extraction

The local LLM attempts to extract:

```json
{
  "people": [],
  "organizations": [],
  "locations": [],
  "dates": []
}
```

### Number Extraction

The system also extracts important numeric information:

```json
[
  {
    "value": "42%",
    "context": "growth rate"
  }
]
```

These results are displayed in the Document Insights interface.

## Example Workflow

```
Upload document
      ↓
Extract document text
      ↓
Split into chunks
      ↓
Generate embeddings
      ↓
Store in ChromaDB
      ↓
Build BM25 index
      ↓
Generate document insights
      ↓
Ask a question
      ↓
Hybrid retrieval
      ↓
Cross-encoder reranking
      ↓
Retrieve top passages
      ↓
Ollama generates grounded answer
      ↓
Display answer + citations
```

## Example Questions

Try questions such as:

What is the main objective of this document?

Summarize the key findings.

What organizations are mentioned?

What are the major risks?

What percentage growth is reported?

What methodology was used?

What are the most important conclusions?
For unsupported questions, the system is designed to avoid inventing an answer and instead indicate that the information was not found in the uploaded documents.

## Data and Storage

Lexora maintains local persistent state for:

```
data/chroma/
data/document_metadata.json
```

The vector database stores the indexed document chunks and associated metadata, while data/document_metadata.json stores document-level information such as:

Chunk count
File hash
Summary
Extracted entities
Key numbers

## Privacy

Lexora is designed around a local-first architecture.

Documents are processed locally and stored in the project's local data directory. The LLM component uses Ollama rather than a hosted API, while embeddings, retrieval, and reranking also run locally.

Note that installing or downloading models may require an internet connection initially.

## Limitations

Processing speed depends on local CPU resources and the selected models.
Large document collections require more memory and storage.
Ollama must be installed and running for LLM-powered analysis and answering.
Extraction quality depends on document structure and the selected local model.
The current implementation is optimized for local single-user document analysis rather than distributed deployment.

## Future Improvements

Potential extensions include:

Streaming responses
Better table and spreadsheet understanding
More advanced document-aware chunking
Multi-document comparison
Conversation-aware retrieval
Document visualization
Additional reranking strategies
GPU acceleration
More granular citation highlighting
Support for additional document formats

## Project Status

**Lexora V1 — Core RAG System Implemented**

Current V1 capabilities include:

- Multi-format document ingestion
- PDF, DOCX, TXT, Markdown, and XLSX support
- Document chunking
- Local embedding generation
- ChromaDB vector storage
- BM25 keyword retrieval
- Hybrid retrieval
- Cross-encoder reranking
- Local Ollama LLM generation
- Generative AI-based document analysis
- Document summarization
- Named-entity extraction
- Important-number extraction
- Source citations
- Streamlit interface
- Document management

## Author

**Sumit Salgotra**

B.Tech Computer Science & Engineering
National Institute of Technology Srinagar

---
