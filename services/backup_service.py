# services/backup_service.py

import os
import shutil
from config.config import BACKUP_FOLDER
from utils.logger import print_info, print_error

class BackupService:
    def backup_file(self, filepath: str) -> None:
        """Cria um backup do arquivo fornecido no diretório de backup."""
        try:
            os.makedirs(BACKUP_FOLDER, exist_ok=True)
            filename = os.path.basename(filepath)
            backup_path = os.path.join(BACKUP_FOLDER, filename)
            shutil.copy(filepath, backup_path)
            print_info(f"Backup criado: {backup_path}")
        except Exception as e:
            print_error(f"Erro ao criar backup de {filepath}: {e}")
