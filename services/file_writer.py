# services/file_writer.py

from utils.logger import print_info, print_error

class FileWriter:
    def save_suggestion(self, filepath: str, suggestion: str) -> None:
        """Salva a sugestão de correção em um arquivo de texto."""
        try:
            suggestion_path = filepath.replace(".py", ".suggestion.txt")
            with open(suggestion_path, 'w', encoding='utf-8') as f:
                f.write(suggestion)
            print_info(f"Sugestão salva em: {suggestion_path}")
        except Exception as e:
            print_error(f"Erro ao salvar sugestão para {filepath}: {e}")
