from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from configs.config import MODEL, DEVICE, VECTOR_DB_DIR
from pypdf import PdfReader
from docx import Document
import chromadb
import shutil
import os


def load_document(file_obj, file_name: str):
    """Load document from a file-like object. Read & extract text from the document."""
    ext = file_name.split('.')[-1].lower()

    if ext == 'pdf':
        pdf_reader = PdfReader(file_obj)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text
    elif ext == 'docx':
        doc = Document(file_obj)
        text = "\n".join([para.text for para in doc.paragraphs])

        return text
    elif ext in ['txt', 'md']:
        text = file_obj.read().decode("utf-8")

        return text


def chunk_document(text: str) -> list[str]:
    """Chunk text into smaller segments with overlap."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=128
    )

    return text_splitter.split_text(text)


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Convert text chunks into embeddings using a transformer model."""
    model = HuggingFaceEmbeddings(
        model_name=MODEL,
        model_kwargs={
            "device": DEVICE
        }
    )

    embeddings = model.embed_documents(chunks)

    return embeddings


def initialize_vector_db(persist_directory: str = VECTOR_DB_DIR, collection_name: str = "documents", delete_existing: bool = True):
    """Initialize a ChromaDB instance and store vectors persistently.

    Args:
        persist_directory: The directory where ChromaDB will persist data. Defaults to "./vector_db"
        collection_name: The name of the collection to create/get. Defaults to "documents"
        delete_existing: Whether to delete the existing database if it exists.

    Returns:
        chromadb.Collection: The ChromaDB collection instance
    """
    if delete_existing and os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)

    os.makedirs(persist_directory, exist_ok=True)

    # Initialize ChromaDB client with persistent storage
    client = chromadb.PersistentClient(path=persist_directory)

    # Create the collection
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "hnsw:space": 'cosine',
            "hnsw:batch_size": 10000
        }
    )

    return collection


def insert_documents(collection: chromadb.Collection, chunks: list[str], embeddings: list[list[float]]):
    """Insert documents and their embeddings into the ChromaDB collection."""
    ids = [f"doc_{i}" for i in range(len(chunks))]
    metadatas = [{"source": f"chunk_{i}"} for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def get_db_collection(file_obj, file_name: str) -> chromadb.Collection:
    """Get the ChromaDB collection for a specific document."""
    document = load_document(file_obj, file_name)
    chunks = chunk_document(document)
    embeddings = embed_chunks(chunks)

    collection = initialize_vector_db()
    insert_documents(collection, chunks, embeddings)

    return collection
