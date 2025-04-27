# services/correction_planner.py

import os

class CorrectionPlanner:
    def __init__(self, project_analyzer):
        self.analyzer = project_analyzer

    def generate_context_for_file(self, filename: str) -> str:
        """Gera um contexto de dependências para o arquivo informado."""
        context = ""

        if filename in self.analyzer.func_calls:
            calls = self.analyzer.func_calls[filename]
            if calls:
                context += "- Este arquivo chama funções de outros arquivos:\n"
                dependencies = self.analyzer.detect_dependencies()
                for function, source_file in dependencies.get(filename, []):
                    module = os.path.splitext(source_file)[0]
                    context += f"  - {function} definida em {module}.py (use 'from {module} import {function}')\n"
                context += "- Importe as funções corretas. Não redefina funções já existentes.\n"
            else:
                context += "- Este arquivo apenas define funções ou classes.\n"

        return context
