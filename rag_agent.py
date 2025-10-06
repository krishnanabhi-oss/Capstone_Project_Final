
# Import Ollama LLM wrapper from LangChain community integrations
from langchain_community.llms import Ollama
# Import Hugging Face sentence-transformers for local embeddings
from sentence_transformers import SentenceTransformer
# Import ChromaDB client for vector database operations
from chromadb import Client
# Import Tool class for LangChain tool abstraction
from langchain.tools import Tool

def retrieve_docs(query, top_k=3):
    # Create a ChromaDB client instance
    client = Client()
    # Get or create a persistent collection for document chunks and embeddings
    collection = client.get_or_create_collection("knowledge_repo")
    # Load the Hugging Face embedding model (MiniLM) for encoding queries
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Generate embedding for the user's query
    query_embedding = model.encode([query])[0].tolist()
    # Query the vector DB for top_k most similar document chunks
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    # Concatenate the retrieved document chunks as context
    return "\n".join([doc for doc in results["documents"][0]])

def generate_answer(context, query):
    # Initialize Ollama LLM wrapper (ensure Ollama is running with the correct model)
    llm = Ollama(model="llama3", base_url="http://localhost:11434")
    # Construct the prompt with retrieved context and user question
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    try:
        # Generate answer using the LLM
        answer = llm(prompt)
    except Exception:
        # Handle any LLM errors gracefully
        answer = "Sorry, I couldn't process your question due to an internal error."
    return answer

def rag_agent(query):
    # Retrieve relevant document context for the user's query
    context = retrieve_docs(query)
    if not context or context.strip() == "":
        # If no relevant context is found, return a fallback message
        return "Sorry, I couldn't find an answer to your question in the uploaded documents."
    # Generate and return the answer using the LLM
    return generate_answer(context, query)

rag_tool = Tool(
    # Define a LangChain Tool for the RAG agent, so it can be used in agent workflows
    name="RAGChatAgent",
    func=rag_agent,
    description="Retrieves relevant context and generates answers using Hugging Face embeddings and Llama 3.2+ (via Ollama)."
)