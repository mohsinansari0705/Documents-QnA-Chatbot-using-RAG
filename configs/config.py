import torch
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VECTOR_DB_DIR = os.path.join(ROOT_DIR, 'vector_db')

PROMPT_CONFIG_FPATH = os.path.join(ROOT_DIR, 'configs', 'prompt_config.yaml')

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM = 'llama-3.1-8b-instant'