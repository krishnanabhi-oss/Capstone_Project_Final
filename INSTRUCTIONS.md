
# Step-by-Step Instructions: Conversational RAG Chatbot (Streamlit + Hugging Face + ChromaDB + Ollama)

## A. Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **Create & activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Llama model weights:**
   - Download the appropriate GGUF/BIN file for Llama 3.2 from Hugging Face, Ollama, or Meta.
   - Place `llama-3.2.bin` in your project root.

---

## B. Ingest Documents

5. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

6. **In the UI:**
   - Upload PDF/TXT files.
   - Click "Ingest Documents" to process and store them in the vector database.

---

## C. Chat with Your Documents

7. **Ask questions in the chatbot interface:**
   - Type your question related to the uploaded documents.
   - Click "Get Answer."

**Process:**
- Your query is embedded using Hugging Face sentence-transformers (MiniLM).
- Top relevant document chunks are retrieved from ChromaDB.
- Context + question are sent to Ollama (Llama3 model) for answer generation.
- Response is shown in UI.

---

## D. Troubleshooting

- **ModuleNotFoundError:**  
  Install the missing package using `pip install <package-name>`.
- **Model not found:**  
  Ensure `llama-3.2.bin` is in the project root.
- **Supported formats:**  
  Only PDF and TXT files are supported for ingestion.

---

## E. Customization

- **Change chunk size:**  
  Edit `chunk_size` in `ingest_agent.py`.
- **Swap embedding model:**  
   Replace Hugging Face MiniLM with another embedding class if desired.
- **Use a different LLM:**  
   Update Ollama model name in `rag_agent.py`.