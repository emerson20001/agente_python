# config/config.py

import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
BACKUP_FOLDER = os.getenv("BACKUP_FOLDER", "backups/")
EXTENSIONS_VALIDAS = tuple(ext.strip() for ext in os.getenv("EXTENSIONS_VALIDAS", ".py").split(","))
