
# Architecture Diagram: Conversational RAG Chatbot

```
+---------------------+         +--------------------+         +------------------+
|   User / Streamlit  | <--->   | Langchain Agents   | <--->   |   Ollama LLM     |
|       (app.py)      |         | (ingest/rag_agent) |         |  (llama3 model)  |
+---------------------+         +--------------------+         +------------------+
           |                              |                            ^
           v                              v                            |
+-------------------------+     +---------------------+       +--------+--------+
| Document Upload (PDF/   | --> | Embedding (HF MiniLM)| ---> | Vector DB (Chroma)|
| TXT via Streamlit)      |     | + Chunking          | <--- |   Retrieval       |
| + PDF Extraction        |     +---------------------+       +------------------+
|   (PyMuPDF/fitz)        |
+-------------------------+
```

**Data Flow:**
* User uploads PDF/TXT files via Streamlit UI.
* Text is extracted and chunked in `ingest_agent.py`.
* Chunks are embedded using Hugging Face sentence-transformers (MiniLM).
* Embeddings and chunks are stored in ChromaDB.
* User asks a question; query is embedded and relevant chunks are retrieved from ChromaDB.
* Context and question are sent to Ollama (Llama3 model) for answer generation.
* Answer is displayed in the Streamlit UI.