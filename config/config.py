# config/config.py

import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    print("\n Biblioteca 'python-dotenv' não encontrada.")
    print(" Execute o comando abaixo para instalar:")
    print("\n    pip install python-dotenv\n")
    exit(1)

# Carrega as variáveis do arquivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
BACKUP_FOLDER = os.getenv("BACKUP_FOLDER", "backups/")
EXTENSIONS_VALIDAS = tuple(ext.strip() for ext in os.getenv("EXTENSIONS_VALIDAS", ".py").split(","))
