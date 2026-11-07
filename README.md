# Local RAG Chatbot with Document Citations & Chat History

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents and ask questions based on their content. It retrieves relevant information from uploaded files and generates context-aware answers with source citations.

The application runs locally using Ollama and Llama 3.2, providing a document-based question-answering experience without depending on a cloud-based LLM API.

## Key Features

- **Document Upload:** Supports PDF, DOCX, and TXT files.
- **Document Processing:** Extracts text and splits it into manageable chunks.
- **Semantic Search:** Uses embeddings and ChromaDB to retrieve relevant document content.
- **RAG Pipeline:** Generates answers grounded in retrieved document context.
- **Source Citations:** Returns document references and supporting text with generated answers.
- **Citation Validation:** Validates whether generated source references exist.
- **Conversation Memory:** Maintains multi-turn conversation history.
- **Persistent Storage:** Uses SQLite and LangGraph checkpointing to preserve conversation state.
- **Local LLM:** Uses Ollama with Llama 3.2 for local inference.
- **REST API:** Exposes document upload and chat functionality through FastAPI.
- **Workflow Orchestration:** Uses LangGraph to coordinate retrieval, generation, and citation validation.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | Ollama – Llama 3.2 |
| LLM Framework | LangChain |
| Workflow Orchestration | LangGraph |
| Backend | FastAPI |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Chat History | SQLite |
| API Documentation | Swagger UI |

## Architecture

```text
                 User
                  |
                  v
             FastAPI
                  |
          +-------+-------+
          |               |
          v               v
     Document Upload    Chat API
          |               |
          v               v
     Document Loader   LangGraph Workflow
          |               |
          v               v
       Chunking        Retrieval
          |               |
          v               v
      Embeddings       ChromaDB
          |               |
          v               v
       ChromaDB       Relevant Context
                          |
                          v
                    Ollama LLM
                     Llama 3.2
                          |
                          v
                   Generated Answer
                          |
                          v
                  Citation Validation
                          |
                          v
                    API Response

          SQLite <--- Conversation Checkpoints
```

## Supported Document Formats

- PDF (`.pdf`)
- Microsoft Word (`.docx`)
- Text (`.txt`)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API availability |
| POST | `/api/upload` | Upload and index documents |
| POST | `/api/chat` | Ask questions and receive cited answers |

## Example API Request

**POST `/api/chat`**

```json
{
  "question": "How many annual leave days are available?",
  "conversation_id": "conversation_001"
}
```

## Example API Response

```json
{
  "conversation_id": "conversation_001",
  "question": "How many annual leave days are available?",
  "answer": "Employees are entitled to 20 days of annual leave per year. [Source 0]",
  "citations": [
    {
      "source_id": 0,
      "source": "uploaded_documents/company_policy.txt",
      "page": null,
      "content": "Employees are entitled to 20 days of annual leave per year."
    }
  ]
}
```

## Project Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ChatBot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Ollama

Download Ollama from:

https://ollama.com/

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2:3b
```

### 6. Start the backend

```bash
python -m uvicorn app.main:app --reload
```

### 7. Open API documentation

Visit:

http://127.0.0.1:8000/docs

Use Swagger UI to upload documents and interact with the chatbot.

## Project Objectives

The primary objectives of this project are:

1. Build a document-based question-answering system using Retrieval-Augmented Generation.
2. Generate answers grounded in uploaded document content.
3. Provide source references and supporting evidence for generated answers.
4. Maintain persistent conversation history across multiple chat interactions.
5. Run the complete AI pipeline locally using an open-source LLM.

## Current Implementation Status

- [x] Document loading
- [x] Text chunking
- [x] Embedding generation
- [x] ChromaDB vector storage
- [x] Semantic document retrieval
- [x] LLM-based answer generation
- [x] Source citation generation
- [x] Citation ID validation
- [x] LangGraph workflow
- [x] SQLite conversation checkpointing
- [x] Multi-turn conversation history
- [x] FastAPI chat endpoint
- [x] Document upload endpoint

## Future Improvements

- Frontend integration with Next.js.
- Document-specific retrieval and filtering.
- Stronger evidence-based citation validation.
- Improved document deduplication and ingestion management.
- Conversation management and history retrieval APIs.

---

**Built with Python, LangChain, LangGraph, FastAPI, ChromaDB, and Ollama.**
