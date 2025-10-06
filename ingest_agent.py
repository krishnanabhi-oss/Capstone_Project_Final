
# Import PyMuPDF for PDF text extraction
import fitz  # PyMuPDF: use 'import fitz' after installing pymupdf
# Import Hugging Face sentence-transformers for local embeddings
from sentence_transformers import SentenceTransformer
# Import ChromaDB client for vector database operations
from chromadb import Client
# Import Tool class for LangChain tool abstraction
from langchain.tools import Tool
# For handling temporary files
import tempfile
# For file extension checks
import os

def is_supported_file_type(file):
    # Supported file types for ingestion
    supported_formats = ['.pdf', '.txt', '.docx']
    file_extension = os.path.splitext(file.name)[1].lower()
    return file_extension in supported_formats


def extract_text(file):
    # Ensure a file is uploaded
    if not file:
        raise ValueError("No file uploaded.")
    # Only allow PDF files for this function
    if not file.name.lower().endswith('.pdf'):
        raise ValueError("File must be a PDF.")
    # If PDF, extract text using PyMuPDF
    if file.name.endswith(".pdf"):
        # PyMuPDF requires a file path, so we need to save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(file.read())
            tmp_pdf.flush()
            try:
                doc = fitz.open(tmp_pdf.name)
                text = ""
                for page in doc:
                    text += page.get_text() or ""
                doc.close()
            except Exception as e:
                print("Error opening file:", e)
                text = None
        return text
    # If TXT, decode and return as string
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return None

def chunk_text(text, chunk_size=500):
    # Split text into chunks of specified size for embedding
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def ingest_documents(files):
    # Ingest uploaded files into the vector database
    for file in files:
        # Check if file type is supported
        if not is_supported_file_type(file):
            raise ValueError(f"Unsupported file format: {file.name}")
    # Create a ChromaDB client instance
    client = Client()
    # Get or create a persistent collection for document chunks and embeddings
    collection = client.get_or_create_collection("knowledge_repo")
    ingested = False
    # Load the Hugging Face embedding model once for efficiency
    model = SentenceTransformer('all-MiniLM-L6-v2')
    for file in files:
        # Extract text from the file
        text = extract_text(file)
        if not text:
            continue
        # Split text into chunks
        chunks = chunk_text(text)
        # Generate embeddings for each chunk
        embeddings = model.encode(chunks).tolist()
        # Add each chunk and its embedding to the vector DB with a unique ID
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            collection.add(
                ids=[f"{file.name}_{i}"],
                embeddings=[embedding],
                documents=[chunk]
            )
        ingested = True
    return ingested

ingest_tool = Tool(
    # Define a LangChain Tool for document ingestion, so it can be used in agent workflows
    name="DocumentIngestion",
    func=ingest_documents,
    description="Ingests PDF/TXT files into the vector DB using Hugging Face embeddings."
)