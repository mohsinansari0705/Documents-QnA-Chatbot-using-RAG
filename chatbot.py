from RAG_pipeline import respond_to_query
from ingest import get_db_collection
import streamlit as st
import requests


st.set_page_config(
    page_title="File Q&A Chatbot",
    page_icon="docs/favicon.png"
)


# Flag variables
if 'valid_api_key' not in st.session_state:
    st.session_state['valid_api_key'] = False
if 'api_success_toast' not in st.session_state:
    st.session_state['api_success_toast'] = False
if 'api_text_input' not in st.session_state:
    st.session_state['api_text_input'] = False
if 'collection_stored' not in st.session_state:
    st.session_state['collection_stored'] = False


# Chatbot sidebar
with st.sidebar:
    st.header("Groq API Key")
    api_key = st.text_input(
        "Enter your API key:",
        key="api_key",
        type="password",
        disabled=st.session_state.get('api_text_input')
    )

    "[Get a Groq API key](https://console.groq.com/keys)"
    "[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/mohsinansari0705/File-QnA-Chatbot-using-RAG)"


# Validate the api_key
if api_key and not st.session_state.get('valid_api_key'):
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        st.session_state['valid_api_key'] = True
        st.session_state['api_success_toast'] = True
        st.session_state['api_text_input'] = True
    else:
        st.toast("Your API key is invalid. Please check it and try again.", icon="❌")

if st.session_state.get('api_success_toast'):
    st.toast("API key is valid. Upload your document to get started.", icon="✅")
    st.session_state['api_success_toast'] = False


# Chatbot main interface
st.title("📝 File Q&A Chatbot using RAG")
if not st.session_state.get('collection_stored'):
    st.markdown(
        """
        This tool uses Retrieval-Augmented Generation (RAG) to answer your questions using the content of your uploaded documents.

        **How to use:**
        1. Upload a document (PDF, DOCX, TXT, or Markdown).
        2. Enter your Groq API key in the sidebar.
        3. Type a question about the document (e.g., "Summarize the main points" or "What are the key findings?").
        4. The chatbot will analyze your document and generate an answer based on its contents.

        Your data is processed securely and only used to answer your questions.
    """
)


# file upload section
uploaded_file = st.file_uploader(
    "Upload a document/file",
    type=['pdf', 'docx', 'txt', 'md'],
    disabled=not st.session_state.get('valid_api_key')
)
if st.session_state.get('valid_api_key') and uploaded_file is not None:
    if 'collection' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner("Processing document..."):
            st.session_state['collection'] = get_db_collection(uploaded_file, uploaded_file.name)
            st.session_state['file_name'] = uploaded_file.name
            st.session_state['collection_stored'] = True
        st.toast("Document uploaded and processed successfully. Now you can ask questions about it.", icon="✅")


# prompt section
prompt = st.text_input(
    "Ask a question about the uploaded file",
    placeholder="Give me a summary of the document.",
    disabled=not st.session_state.get('collection_stored')
)
if st.session_state.get('valid_api_key') and st.session_state.get('collection_stored') and prompt:
    collection = st.session_state['collection']
    with st.spinner("Generating response..."):
        response = respond_to_query(collection, api_key, prompt)
    
    st.write(response)


if not st.session_state.get('valid_api_key'):
    st.info("Please first enter your API key to proceed.")
if st.session_state.get('valid_api_key') and not st.session_state.get('collection_stored'):
    st.info("Please upload a document to proceed.")