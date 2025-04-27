# services/file_scanner.py

import os
from config.config import EXTENSIONS_VALIDAS
from models.file_model import CodeFile

class FileScanner:
    def __init__(self, root_folder: str):
        self.root_folder = root_folder

    def scan_all_files(self) -> list[CodeFile]:
        """Percorre a pasta raiz e retorna uma lista de arquivos de código."""
        code_files = []
        for root, _, files in os.walk(self.root_folder):
            for file in files:
                if file.endswith(EXTENSIONS_VALIDAS):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    code_files.append(CodeFile(full_path, content))
        return code_files
