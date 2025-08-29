# RAG-powered-AI-chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with [LangChain](https://python.langchain.com/), [Streamlit](https://streamlit.io/), and [Chroma](https://www.trychroma.com/). This chatbot answers questions based on custom PDF documents.

## Project contribution 

This project was collaboratively built by [Sahil Nayak](https://github.com/sahilk12nayak), [Ankur Mishra](https://github.com/ankur110), [Iryna Lukysha](https://github.com/IrynaL-dev), and [Oluwajuwon](https://github.com/Oluwajuwon-O).

We worked together through a shared GitHub repository to design and implement the complete RAG-powered chatbot using LangChain, Streamlit, and a vector store. From document ingestion to LLM integration, and all components were collaboratively developed.

Our discussions, planning, and problem-solving were conducted primarily via Google Meet, which allowed us to align on architecture decisions, debug issues together, and maintain a smooth development workflow throughout the project.

## Project Structure
```
rag_chatbot/
│
├── docs/ # Place your PDF documents here
├── embeddings/ # Chroma vector DB storage
├── ingest.py # Script to process & store document embeddings
├── main.py # Streamlit app
├── rag_pipeline.py # LangChain pipeline setup
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

## Features

- Upload and ingest custom PDF documents
- Ask questions in natural language
- Responses are grounded in the ingested documents
- Cites source documents in the response
- Built with modular LangChain pipeline
- Streamlit-based minimal web UI


## Steps:
```
1. Create virtual environment commands
   python3 -m venv myenv
   source myenv/bin/activate
2. Install dependencies command
   python install -r requirement.txt
3. Add your document
   Put your .pdf files inside the docs/ folder.
4. Ingest documents command
   python ingest.py
5. Set your LLM API key
   export GOOGLE_API_KEY="your-gemini-api-key"
6. Run the chatbot
   streamlit run main.py
```

## Results:
![image](https://github.com/user-attachments/assets/8e9b828c-58d5-4a7a-972d-cba73588b640)
![image](https://github.com/user-attachments/assets/017b8667-320f-447c-8de7-39cc1f1e529d)
![image](https://github.com/user-attachments/assets/23347640-0963-4e85-8641-445559eb4a6e)

 License: [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) — Open source. 

