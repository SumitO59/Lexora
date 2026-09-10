# Lexora — Project Development Plan & Technical Documentation

## 1. Project Overview

**Project:** Lexora  
**Tagline:** Privacy-First Local RAG Platform  
**Primary Goal:** Rebuild the current Lexora repository as a faithful V1 implementation, understand every major component while developing it, validate the complete pipeline, and only then add original improvements.

### Resume Target

> **Lexora – Privacy-First Local RAG Platform | Python, Ollama, LangChain, ChromaDB, Streamlit | GitHub**
>
> - Built a local RAG platform for PDF, DOCX, XLSX, TXT, and Markdown question answering using hybrid retrieval with ChromaDB vector search and BM25 keyword search.
> - Implemented cross-encoder reranking and grounded generation with a local Ollama LLM to improve retrieval relevance and keep document processing and inference local.
> - Added automated document summarization, named-entity and key-number extraction, and source citations with document, page, chunk, and retrieval confidence metadata.

---

# 2. Development Philosophy

Lexora will be developed in two major versions.

## V1 — Baseline / Alignment

The objective is to reproduce the behavior and architecture of the existing Lexora repository as closely as possible.

We will NOT prematurely add:
- New frameworks
- Cloud APIs
- Authentication
- React/FastAPI
- Agents
- LangGraph
- Cloud vector databases
- Streaming
- Multi-user functionality
- Unrequested UI redesigns

The V1 implementation should contain the same core:
- Supported document formats
- Document loading
- Chunking
- Embedding model
- ChromaDB storage
- BM25 retrieval
- Hybrid retrieval
- Cross-encoder reranking
- Ollama generation
- Grounded prompting
- Citations
- Document summaries
- Entity extraction
- Key-number extraction
- Document management
- Streamlit interface

## V2 — Original Improvements

Only after V1 is fully working and validated will we evaluate improvements.

Potential V2 directions:
- Better table/spreadsheet understanding
- Improved document-aware chunking
- Multi-document comparison
- Conversation-aware retrieval
- Streaming
- Better citation highlighting
- Retrieval evaluation
- GPU acceleration
- Improved metadata handling
- Better document visualization
- Additional retrieval/reranking strategies

V2 features must be selected based on technical value, learning value, resume value, and feasibility.

---

# 3. Target Architecture

```text
                         ┌──────────────────────┐
                         │    Streamlit UI      │
                         │                      │
                         │ Upload / Chat /      │
                         │ Document Insights    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      RAGEngine       │
                         │   Pipeline Manager   │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │   Loaders    │    │  Retrieval   │    │   Analysis   │
        │              │    │              │    │              │
        │ PDF          │    │ ChromaDB     │    │ Summary      │
        │ DOCX         │    │ BM25         │    │ Entities     │
        │ TXT          │    │ Hybrid       │    │ Key Numbers  │
        │ MD           │    │ Reranking    │    │              │
        │ XLSX         │    │              │    │              │
        └──────────────┘    └──────────────┘    └──────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Ollama Local LLM  │
                         │  Grounded Generation │
                         └──────────────────────┘
```

---

# 4. Target Project Structure

```text
Lexora/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── chroma_db/
├── doc_meta.json
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── loaders.py
    ├── retrieval.py
    ├── analysis.py
    ├── utils.py
    └── engine.py
```

### Responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Streamlit application and UI |
| `config.py` | Paths, models, chunking constants |
| `loaders.py` | Document loading and text splitting |
| `retrieval.py` | ChromaDB, BM25, hybrid search, reranking |
| `analysis.py` | Summary/entity/key-number extraction |
| `utils.py` | File hashing and utility functions |
| `engine.py` | Main RAG orchestration |
| `__init__.py` | Package exports |

---

# 5. Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Frontend/UI | Streamlit |
| RAG framework | LangChain |
| Embeddings | Hugging Face |
| Embedding model | `BAAI/bge-small-en-v1.5` |
| Vector database | ChromaDB |
| Keyword retrieval | BM25 / `rank_bm25` |
| Reranking | Sentence Transformers CrossEncoder |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| LLM runtime | Ollama |
| Default LLM | `llama3` |
| PDF loading | PyPDFLoader |
| DOCX loading | Docx2txtLoader |
| TXT/MD loading | TextLoader |
| XLSX loading | UnstructuredExcelLoader |
| Numerical processing | NumPy |
| Persistence | ChromaDB + `doc_meta.json` |

---

# 6. Phase 0 — Environment & Repository Setup

## Objective

Create a clean development environment and confirm all local dependencies work before implementing application features.

## Tasks

- Clone/access Lexora repository.
- Create Python virtual environment.
- Activate virtual environment.
- Install dependencies.
- Verify Python version.
- Install Ollama.
- Verify Ollama is running.
- Pull baseline model.
- Verify Streamlit installation.
- Establish clean Git working state.

## Features / Deliverables

```text
[ ] Python environment
[ ] Virtual environment
[ ] requirements installed
[ ] Ollama installed
[ ] llama3 available
[ ] Streamlit launches
[ ] Git repository ready
```

## Learning Topics

- Python virtual environments
- Python packages
- `pip`
- imports/modules
- environment isolation
- basic Git workflow

## Learning Resources

- Python `venv`: https://docs.python.org/3/library/venv.html
- Python Packaging User Guide: https://packaging.python.org/
- Ollama documentation: https://docs.ollama.com/
- Streamlit documentation: https://docs.streamlit.io/

## Exit Criteria

The environment can run a minimal Streamlit application and Ollama responds to a local model request.

---

# 7. Phase 1 — Configuration Layer

## Objective

Create the central configuration used by every component.

## Features

Implement:

```text
CHROMA_DIR
META_PATH
EMBED_MODEL
RERANK_MODEL
OLLAMA_MODEL
CHUNK_SIZE
CHUNK_OVERLAP
```

Baseline values:

```text
Embedding:
BAAI/bge-small-en-v1.5

Reranker:
cross-encoder/ms-marco-MiniLM-L-6-v2

Default LLM:
llama3

Chunk size:
512

Chunk overlap:
64
```

## Learning Topics

- `pathlib`
- Python modules
- constants
- configuration management

## Exit Criteria

All major configuration values are centralized and no component needs hard-coded model/path values.

---

# 8. Phase 2 — Document Loading

## Objective

Build the ingestion layer for all supported file formats.

## Supported Formats

```text
PDF
DOCX
TXT
MD
XLSX
```

## Features

- Extension detection
- Loader selection
- Document extraction
- Metadata preservation
- Unsupported-format handling

## Pipeline

```text
Uploaded File
     ↓
Extension Detection
     ↓
Loader Selection
     ↓
LangChain Documents
```

## Learning Topics

- LangChain `Document`
- document loaders
- file handling
- metadata
- parsing

## Learning Resources

- LangChain: https://python.langchain.com/docs/introduction/
- LangChain document loaders: https://python.langchain.com/docs/integrations/document_loaders/

## Exit Criteria

Every supported format successfully loads into a list of LangChain `Document` objects.

---

# 9. Phase 3 — Text Chunking

## Objective

Split loaded documents into retrieval-friendly chunks.

## Baseline Configuration

```text
Chunk size: 512
Overlap: 64
```

## Features

- Recursive character splitting
- Preserve document metadata
- Attach chunk index
- Maintain page information where available

## Pipeline

```text
Document
   ↓
RecursiveCharacterTextSplitter
   ↓
Chunks
   ↓
Chunk metadata
```

## Learning Topics

- Chunking
- chunk size
- chunk overlap
- token vs character length
- retrieval-oriented preprocessing
- metadata propagation

## Learning Resource

https://python.langchain.com/docs/concepts/text_splitters/

## Exit Criteria

A document can be transformed into correctly indexed chunks with source/page/chunk metadata.

---

# 10. Phase 4 — Embeddings

## Objective

Convert chunks into vector representations.

## Baseline Model

```text
BAAI/bge-small-en-v1.5
```

## Features

- Load Hugging Face embedding model.
- CPU-based embedding.
- Normalize embeddings.
- Generate embeddings for document chunks.
- Generate query embeddings.

## Pipeline

```text
Text Chunk
    ↓
Embedding Model
    ↓
Vector
```

## Learning Topics

- Embeddings
- vector representations
- semantic similarity
- cosine similarity
- normalization

## Learning Resources

- Sentence Transformers: https://www.sbert.net/
- Hugging Face: https://huggingface.co/docs

## Exit Criteria

Chunks can be embedded locally and vectors can be generated consistently.

---

# 11. Phase 5 — ChromaDB Vector Storage

## Objective

Persist document embeddings and metadata locally.

## Features

- Create/open persistent ChromaDB collection.
- Store chunks.
- Store embeddings.
- Store metadata.
- Similarity search.
- Retrieve indexed documents.
- Delete document chunks.
- Persist data between application restarts.

## Storage

```text
chroma_db/
```

## Pipeline

```text
Chunks
  ↓
Embeddings
  ↓
ChromaDB
```

## Learning Topics

- vector databases
- similarity search
- persistent storage
- metadata filtering
- vector indexing

## Learning Resource

https://docs.trychroma.com/

## Exit Criteria

The application can index chunks, restart, reopen ChromaDB, and retrieve the same data.

---

# 12. Phase 6 — BM25 Keyword Retrieval

## Objective

Implement lexical retrieval alongside semantic search.

## Features

- Build BM25 index from indexed chunks.
- Tokenize documents.
- Tokenize query.
- Calculate BM25 scores.
- Return top-k lexical matches.
- Rebuild BM25 after indexing/deletion.

## Pipeline

```text
Query
  ↓
BM25
  ↓
Top-k keyword matches
```

## Learning Topics

- Information retrieval
- inverted indexes
- TF
- IDF
- BM25
- lexical retrieval vs semantic retrieval

## Learning Resources

- Introduction to Information Retrieval: https://nlp.stanford.edu/IR-book/
- rank_bm25: https://github.com/dorianbrown/rank_bm25

## Exit Criteria

Exact terminology and keyword-heavy queries can retrieve relevant chunks even when semantic similarity is weaker.

---

# 13. Phase 7 — Hybrid Retrieval

## Objective

Combine semantic and lexical retrieval.

## Features

- Run ChromaDB similarity search.
- Run BM25 search.
- Merge results.
- Remove duplicates.
- Maintain document metadata.
- Produce candidate pool for reranking.

## Pipeline

```text
                 Query
                   │
          ┌────────┴────────┐
          ▼                 ▼
      ChromaDB            BM25
      Semantic            Lexical
          │                 │
          └────────┬────────┘
                   ▼
              Merge/Dedup
                   ↓
             Candidate Pool
```

## Learning Topics

- hybrid search
- retrieval recall
- candidate generation
- semantic + lexical retrieval

## Exit Criteria

Both retrieval strategies contribute candidates to a single retrieval pool.

---

# 14. Phase 8 — Cross-Encoder Reranking

## Objective

Improve ordering of retrieved candidates using a cross-encoder.

## Baseline Model

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

## Features

- Build query-passage pairs.
- Score candidates.
- Sort by cross-encoder score.
- Return top-n results.

## Pipeline

```text
Hybrid Candidate Pool
        ↓
Query + Passage Pairs
        ↓
Cross Encoder
        ↓
Scores
        ↓
Sorted Results
        ↓
Top-k Context
```

## Learning Topics

- bi-encoder vs cross-encoder
- reranking
- query-passage relevance
- retrieval precision

## Learning Resource

https://www.sbert.net/examples/cross_encoder/applications/README.html

## Exit Criteria

The retrieval pipeline returns reranked passages rather than simply using raw vector/BM25 ordering.

---

# 15. Phase 9 — Local Ollama Generation

## Objective

Use a local LLM to generate answers from retrieved context.

## Baseline

```text
Ollama
Default model: llama3
Temperature: 0.1
```

Available UI choices:

```text
llama3
mistral
phi3
gemma2
```

## Features

- Local model connection.
- Model selection.
- Prompt construction.
- Context injection.
- Answer generation.
- Model reuse/caching.

## Learning Topics

- LLM inference
- prompt templates
- temperature
- context windows
- local inference

## Learning Resources

- Ollama: https://docs.ollama.com/
- LangChain Ollama integration: https://python.langchain.com/docs/integrations/llms/ollama/

## Exit Criteria

A question plus retrieved context produces an answer using only the local Ollama model.

---

# 16. Phase 10 — Grounded RAG Q&A

## Objective

Connect retrieval and generation into the complete RAG pipeline.

## Features

- Accept natural-language question.
- Retrieve candidate documents.
- Rerank.
- Build context.
- Generate grounded answer.
- Reject unsupported questions.
- Return source information.

## Grounding Rule

The LLM must be instructed to answer only from retrieved context.

If the answer is unavailable:

```text
Not found in the uploaded documents.
```

## Full Pipeline

```text
User Question
      ↓
Hybrid Retrieval
      ↓
Candidate Pool
      ↓
Cross-Encoder
      ↓
Top-k Context
      ↓
Grounded Prompt
      ↓
Ollama
      ↓
Answer
```

## Exit Criteria

The system answers document-based questions and does not intentionally rely on outside knowledge.

---

# 17. Phase 11 — Source Citations

## Objective

Make every generated answer traceable to source passages.

## Citation Metadata

Each citation should expose:

```text
source
page
chunk
score/confidence
passage
```

## UI

```text
Sources: report.pdf

Sources (3)

[1] report.pdf
Page 4 | Confidence 87%
Relevant passage...

[2] report.pdf
Page 6 | Confidence 82%
Relevant passage...
```

## Learning Topics

- metadata
- provenance
- traceability
- retrieval scores
- citation design

## Exit Criteria

Users can inspect which document/page/chunk supplied the retrieved context.

---

# 18. Phase 12 — Document Analysis

## Objective

Generate automatic document insights during indexing.

## Features

### Summary

Generate a concise 3–5 sentence summary.

### Named Entities

Extract:

```text
People
Organizations
Locations
Dates
```

### Key Numbers

Extract:

```text
Statistics
Percentages
Monetary values
Important numerical facts
```

Example:

```json
{
  "people": [],
  "organizations": [],
  "locations": [],
  "dates": []
}
```

```json
[
  {
    "value": "42%",
    "context": "growth rate"
  }
]
```

## Learning Topics

- structured LLM output
- JSON extraction
- entity extraction
- prompt design
- parsing model output

## Exit Criteria

Each indexed document receives summary, entities, and key-number metadata.

---

# 19. Phase 13 — Document Management

## Objective

Allow users to manage the local index.

## Features

- Show indexed documents.
- Show total chunk count.
- Delete individual documents.
- Re-upload/replace existing documents.
- Persist metadata.
- Maintain file hash.
- Rebuild BM25 after modifications.

## Duplicate Handling

```text
Upload existing document
        ↓
Identify existing source
        ↓
Delete previous chunks
        ↓
Index new chunks
        ↓
Update metadata
```

## Exit Criteria

Index remains consistent after upload, replacement, deletion, and application restart.

---

# 20. Phase 14 — Streamlit UI

## Objective

Connect all backend functionality into the final V1 interface.

## Sidebar

```text
Lexora

100% Local
No API calls

Ollama model
[ llama3 ]

Chunks to retrieve
[ slider ]

Upload Documents
[ uploader ]

Indexed files
file1.pdf       X
file2.docx      X

Clear chat history
```

## Main Interface

Two tabs:

```text
Chat
Document Insights
```

### Chat Features

- Chat history
- User questions
- Assistant answers
- Source tags
- Expandable citations
- Confidence display
- Passage preview

### Document Insights Features

- Document name
- Chunk count
- Summary
- Entities
- Key numbers

## Learning Resource

https://docs.streamlit.io/

## Exit Criteria

A user can complete the entire workflow from the UI without manually calling backend functions.

---

# 21. Phase 15 — RAGEngine Integration

## Objective

Ensure all backend modules operate as one coherent system.

## RAGEngine Responsibilities

```text
Initialize:
    embeddings
    ChromaDB
    splitter
    HybridRetriever
    metadata

Index:
    load
    split
    hash
    metadata
    store
    rebuild BM25
    analyze
    persist metadata

Query:
    retrieve
    rerank
    build context
    generate
    build citations

Delete:
    delete vectors
    delete metadata
    rebuild BM25

Stats:
    files
    chunks

Metadata:
    document insights
```

## Exit Criteria

The entire application can be controlled through a clean central `RAGEngine`.

---

# 22. Phase 16 — Testing & Validation

This phase is mandatory before calling V1 complete.

## Test 1 — PDF

Upload PDF and ask a factual question.

Expected:
- Correct answer
- Correct page
- Correct source

## Test 2 — DOCX

Verify text extraction and Q&A.

## Test 3 — TXT/Markdown

Verify plain-text indexing and retrieval.

## Test 4 — XLSX

Verify spreadsheet content can be loaded and retrieved.

## Test 5 — Semantic Retrieval

Ask a question where the exact query words do not appear in the relevant passage.

Expected:
- Semantic retrieval finds relevant content.

## Test 6 — Keyword Retrieval

Use a specific technical term or identifier.

Expected:
- BM25 retrieves exact terminology.

## Test 7 — Hybrid Retrieval

Use a query benefiting from both semantic and lexical matching.

Expected:
- Relevant candidate pool.

## Test 8 — Reranking

Inspect retrieved candidates and confirm cross-encoder ordering.

## Test 9 — Unsupported Question

Ask something absent from the documents.

Expected:

```text
Not found in the uploaded documents.
```

## Test 10 — Multi-document Retrieval

Upload multiple documents and ask a question answered by only one.

Expected:
- Correct document citation.

## Test 11 — Duplicate Upload

Upload the same document twice.

Expected:
- No duplicated chunks.
- Existing representation replaced.

## Test 12 — Deletion

Delete a document.

Expected:
- Its chunks disappear from retrieval.
- Its metadata disappears.

## Test 13 — Persistence

Restart application.

Expected:
- Indexed documents remain available.

## Test 14 — Model Switching

Switch between Ollama models.

Expected:
- Selected model generates the answer.

---

# 23. Phase 17 — Performance & Reliability Review

Before V1 completion, inspect:

- startup time
- embedding model loading
- reranker loading
- Ollama response time
- memory usage
- large-document behavior
- multiple-document indexing
- error handling
- malformed files
- empty documents
- unsupported files
- corrupted documents

## Error Handling

The application should fail gracefully for:
- unsupported extensions
- unreadable files
- empty documents
- unavailable Ollama
- missing model
- malformed metadata
- ChromaDB errors

---

# 24. Phase 18 — Documentation & Final V1

## README Requirements

Document:

- Project overview
- Features
- Architecture
- Tech stack
- Installation
- Ollama setup
- Running the application
- Retrieval pipeline
- Document analysis
- Example questions
- Storage
- Privacy
- Limitations
- Future improvements

## Final V1 Checklist

```text
DOCUMENT INGESTION
[ ] PDF
[ ] DOCX
[ ] TXT
[ ] Markdown
[ ] XLSX

PROCESSING
[ ] Document loading
[ ] Chunking
[ ] Metadata
[ ] File hashing

RETRIEVAL
[ ] Embeddings
[ ] ChromaDB
[ ] BM25
[ ] Hybrid retrieval
[ ] Cross-encoder reranking

GENERATION
[ ] Ollama
[ ] Model selection
[ ] Grounded prompt
[ ] Unsupported-question handling

CITATIONS
[ ] Document
[ ] Page
[ ] Chunk
[ ] Confidence
[ ] Passage

ANALYSIS
[ ] Summary
[ ] People
[ ] Organizations
[ ] Locations
[ ] Dates
[ ] Key numbers

MANAGEMENT
[ ] Indexed file list
[ ] Chunk counts
[ ] Delete
[ ] Replace/re-upload
[ ] Persistent metadata
[ ] Persistent ChromaDB

UI
[ ] Sidebar
[ ] Upload
[ ] Chat
[ ] Chat history
[ ] Sources
[ ] Document Insights
[ ] Model selector
[ ] Retrieval-k selector

QUALITY
[ ] Error handling
[ ] Testing
[ ] README
[ ] Clean requirements
[ ] Clean Git history
```

---

# 25. Git Milestone Strategy

Each major working stage should produce a meaningful commit.

Suggested commits:

```text
chore: initialize Lexora development environment
feat: add centralized configuration
feat: implement multi-format document loaders
feat: add document chunking pipeline
feat: integrate local embedding model
feat: add persistent ChromaDB vector store
feat: implement BM25 retrieval
feat: implement hybrid retrieval
feat: add cross-encoder reranking
feat: integrate Ollama local generation
feat: implement grounded document Q&A
feat: add source citations
feat: add document analysis
feat: add document management
feat: build Streamlit interface
test: validate end-to-end RAG pipeline
docs: finalize Lexora documentation
```

Commit after a feature is working, not after every small code edit.

---

# 26. Learning Roadmap

The project should be used as a practical learning path.

## Level 1 — Python

Learn:
- modules
- classes
- type hints
- pathlib
- JSON
- file handling
- exceptions
- virtual environments

Resources:
- https://docs.python.org/3/tutorial/
- https://docs.python.org/3/library/pathlib.html

## Level 2 — LangChain

Learn:
- Documents
- loaders
- splitters
- prompts
- model integrations
- vector stores

Resource:
- https://python.langchain.com/docs/introduction/

## Level 3 — Embeddings

Learn:
- vector representation
- similarity
- cosine similarity
- embedding models

Resources:
- https://www.sbert.net/
- https://huggingface.co/docs

## Level 4 — Information Retrieval

Learn:
- lexical search
- TF-IDF
- BM25
- semantic search
- hybrid search
- reranking

Resource:
- https://nlp.stanford.edu/IR-book/

## Level 5 — RAG

Learn:
- ingestion
- indexing
- retrieval
- reranking
- context construction
- grounded generation
- hallucination control

Resource:
- https://python.langchain.com/docs/concepts/rag/

## Level 6 — Local LLMs

Learn:
- Ollama
- model serving
- inference
- temperature
- context windows
- prompt design

Resource:
- https://docs.ollama.com/

## Level 7 — Streamlit

Learn:
- state
- widgets
- file upload
- chat interface
- caching
- tabs
- session state

Resource:
- https://docs.streamlit.io/

---

# 27. V1 Architecture Freeze

Before beginning V1 implementation, the following should remain fixed unless a real technical blocker appears:

```text
Python
Streamlit
LangChain
ChromaDB
Hugging Face embeddings
BAAI/bge-small-en-v1.5
BM25
rank_bm25
Sentence Transformers
cross-encoder/ms-marco-MiniLM-L-6-v2
Ollama
llama3
512 chunk size
64 chunk overlap
```

Any deviation should be explicitly discussed before implementation.

---

# 28. V2 — Improvement Evaluation

Only after V1 passes all tests.

Potential improvements will be evaluated using four criteria:

| Criterion | Question |
|---|---|
| Technical value | Does it materially improve the system? |
| Learning value | Does it teach an important engineering concept? |
| Resume value | Does it make the project stronger? |
| Complexity | Is the improvement worth its implementation cost? |

Potential V2 features:

### Retrieval
- Reciprocal Rank Fusion
- better hybrid-score fusion
- query expansion
- metadata-aware retrieval
- improved reranking

### Documents
- improved spreadsheet/table understanding
- document-aware chunking
- OCR
- structured extraction

### UX
- streaming responses
- highlighted citations
- document previews
- retrieval inspection/debug panel

### RAG
- conversation-aware retrieval
- multi-document comparison
- follow-up questions
- answer confidence
- retrieval evaluation

### Performance
- GPU support
- model caching
- batch embedding
- incremental indexing

---

# 29. V2 Must Not Break V1

Every V2 feature must preserve:

```text
Local-first architecture
       +
Grounded answers
       +
Source traceability
       +
Existing supported formats
       +
Persistent indexing
```

V2 should extend the system rather than replace its core identity.

---

# 30. Final Project Definition

At the end of V1, Lexora should provide this complete workflow:

```text
                    USER
                     │
                     ▼
              Upload Documents
                     │
                     ▼
             Format Detection
                     │
                     ▼
             Document Loading
                     │
                     ▼
                Chunking
                     │
                     ▼
              File Hashing
                     │
                     ▼
              Embeddings
                     │
                     ▼
               ChromaDB
                     │
                     ├───────────────┐
                     ▼               ▼
                   BM25        Vector Search
                     │               │
                     └───────┬───────┘
                             ▼
                       Hybrid Merge
                             │
                             ▼
                     Cross-Encoder
                       Reranking
                             │
                             ▼
                       Top-k Context
                             │
                             ▼
                         Ollama
                             │
                             ▼
                     Grounded Answer
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                Citations        Chat Response


During indexing:
Document
   ├── Summary
   ├── Entities
   └── Key Numbers
          ↓
   Document Insights
```

## V1 Success Definition

Lexora V1 is complete when a user can:

1. Upload PDF, DOCX, XLSX, TXT, or Markdown.
2. Have the document processed entirely locally.
3. Have its chunks embedded and persisted in ChromaDB.
4. Search using both semantic and lexical retrieval.
5. Have candidates reranked using a cross-encoder.
6. Ask natural-language questions.
7. Receive grounded answers from a local Ollama model.
8. Receive source citations with document/page/chunk/confidence metadata.
9. View automatic summaries, entities, and key numbers.
10. Delete or replace indexed documents.
11. Restart the application without losing the local index.

Only after all ten work reliably should we move to V2.

---

# 31. Working Protocol for Development Sessions

For every implementation session:

```text
1. Identify the current phase.
2. Study the assigned resources.
3. Inspect the relevant existing repository code.
4. Identify the exact files to create/edit.
5. Implement one small working feature.
6. Run a focused test.
7. Debug if required.
8. Run the phase-level test.
9. Commit the working change.
10. Move to the next phase.
```

The assistant should provide:
- exact file to open
- whether to create/edit/replace
- relevant code
- commands to run
- expected output
- test procedure
- learning resources for the current concept
- Git commit message

The assistant should NOT provide a large unexplained code dump covering multiple future phases.

---

# 32. Current Starting Point

**Current phase:** Phase 0 — Environment & Repository Setup

**Immediate goal:**

```text
Repository
   ↓
Python environment
   ↓
Dependencies
   ↓
Ollama
   ↓
llama3
   ↓
Streamlit
   ↓
Ready for Phase 1
```

Do not implement RAG functionality until the development environment is verified.
