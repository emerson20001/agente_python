# services/correction_planner.py

import os

class CorrectionPlanner:
    def __init__(self, project_analyzer):
        self.analyzer = project_analyzer

    def generate_context_for_file(self, filename: str) -> str:
        """Gera um contexto de dependências e instruções para o arquivo informado."""
        context = ""

        if filename in self.analyzer.func_calls:
            calls = self.analyzer.func_calls[filename]
            dependencies = self.analyzer.detect_dependencies()

            if calls:
                context += "- Este arquivo faz chamadas para funções de outros arquivos.\n"
                if dependencies.get(filename):
                    for function, source_file in dependencies.get(filename, []):
                        module = os.path.splitext(source_file)[0]
                        context += f"  - Função '{function}' definida em '{module}.py' (importe corretamente com 'from {module} import {function}').\n"
                context += "- Garanta que todas as funções externas estejam corretamente importadas.\n"
                context += "- Não redefina funções ou classes que já existam em outros arquivos.\n"
            else:
                context += "- Este arquivo contém apenas definições de funções ou classes, sem chamadas externas.\n"
                context += "- Foque em corrigir e melhorar apenas o que está dentro deste arquivo.\n"

        else:
            context += "- Não foram detectadas chamadas externas neste arquivo.\n"
            context += "- Corrija apenas definições internas de funções, classes e estruturas.\n"

        return context
