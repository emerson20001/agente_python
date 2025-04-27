# services/project_analyzer.py

import ast
from utils.logger import print_error

class ProjectAnalyzer:
    def __init__(self):
        self.func_definitions = {}
        self.func_calls = {}
        self.class_definitions = {}

    def analyze_file(self, code: str, filename: str) -> None:
        """Analisa um arquivo e mapeia funções, chamadas e classes."""
        try:
            tree = ast.parse(code)
            functions, calls, classes = [], [], []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.Call) and hasattr(node.func, 'id'):
                    calls.append(node.func.id)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            self.func_definitions[filename] = functions
            self.func_calls[filename] = calls
            self.class_definitions[filename] = classes

        except Exception as e:
            print_error(f"Erro ao analisar {filename}: {e}")

    def detect_dependencies(self) -> dict:
        """Detecta dependências entre arquivos com base em funções chamadas."""
        dependencies = {}
        for file, calls in self.func_calls.items():
            for call in calls:
                for other_file, defs in self.func_definitions.items():
                    if other_file != file and call in defs:
                        dependencies.setdefault(file, []).append((call, other_file))
        return dependencies
