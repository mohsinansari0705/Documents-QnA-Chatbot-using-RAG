from prompt_builder import build_prompt_from_config, load_yaml_config
from configs.config import LLM, PROMPT_CONFIG_FPATH
from langchain_groq import ChatGroq
from ingest import embed_chunks


def retrieve_relevant_documents(collection, query: str, n_results: int = 5, threshold: float = 0.5) -> list[str]:
    """Query the ChromaDB database with a string query.

    Args:
        collection (chromadb.Collection): The database collection to query.
        query (str): The search query string
        n_results (int): Number of results to return (default: 5)
        threshold (float): Threshold for the cosine similarity score (default: 0.3)

    Returns:
        dict: Query results containing ids, documents, and metadata
    """
    relevant_results = {
        "ids": [],
        "documents": [],
        "distances": []
    }

    query_embedding = embed_chunks([query])[0]

    # Query the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=['documents', 'distances']
    )

    for i, distance in enumerate(results["distances"][0]):
        if distance < threshold:
            relevant_results["ids"].append(results["ids"][0][i])
            relevant_results["documents"].append(results["documents"][0][i])
            relevant_results["distances"].append(results["distances"][0][i])

    return relevant_results["documents"]


def respond_to_query(collection, api_key, query: str) -> str:
    """Respond to a user query by retrieving relevant documents and building a prompt.
    
    Args:
        collection (chromadb.Collection): The database collection to query.
        api_key (str): The API key for authentication.
        query (str): The user's query string.

    Return:
        str: The response to the user's query.
    """
    relevant_documents = retrieve_relevant_documents(collection, query)

    prompt_config = load_yaml_config(PROMPT_CONFIG_FPATH)

    chatbot_prompt = build_prompt_from_config(
        prompt_config['file_q&a_chatbot_system_prompt'],
        relevant_documents,
        query
    )

    llm = ChatGroq(
        model=LLM,
        temperature=0.7,
        api_key=api_key
    )

    response = llm.invoke(chatbot_prompt)

    return response.content
