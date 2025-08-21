import streamlit as st

st.set_page_config(
    page_title="File Q&A Chatbot",
    page_icon="docs/gc_logo.png"
)

with st.sidebar:
    api_key = st.text_input("Enter your API key:", key="api_key_input", type="password")

    "[Get an OpenAI API key](https://platform.openai.com/api-keys)"
    "[Get a Groq API key](https://console.groq.com/keys)"

    "[![Open in GitHub](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"