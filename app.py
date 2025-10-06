
# Import Streamlit for web UI
import streamlit as st
# Import the document ingestion tool
from ingest_agent import ingest_tool
# Import the RAG chatbot tool
from rag_agent import rag_tool


# Set Streamlit page configuration and title
st.set_page_config(page_title="Conversational RAG Chatbot (Agents)", layout="wide")
st.title("Conversational RAG Chatbot (Langchain Agents + Hugging Face)")


# ---------- Document Upload Section ----------
# Section for uploading and ingesting documents
st.header("Upload Documents (PDF or TXT)")
uploaded_files = st.file_uploader("Choose PDF/TXT files", accept_multiple_files=True)

# Ingest documents when button is clicked
if st.button("Ingest Documents") and uploaded_files:
    success = ingest_tool.func(uploaded_files)
    if success:
        st.success("Documents ingested successfully!")
    else:
        st.error("Failed to ingest documents. Please check file formats.")


# ---------- Chat Interface Section ----------
# Section for user to ask questions about uploaded documents
st.header("Chatbot Interface")
query = st.text_input("Ask a question about your documents:")

# Get answer from RAG chatbot when button is clicked
if st.button("Get Answer") and query:
    response = rag_tool.func(query)
    st.markdown(f"**Bot:** {response}")


# Footer note for user guidance
st.markdown("""
*Note: Only PDF/TXT files are supported for uploads.  
Embeddings powered by Hugging Face sentence-transformers. PDF extraction uses PyMuPDF (fitz).*
""")