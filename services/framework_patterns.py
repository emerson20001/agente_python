# services/framework_patterns.py

import re

class FrameworkPatterns:
    @staticmethod
    def detect_framework(code: str) -> str:
        """Detecta o framework utilizado no código."""
        code_lower = code.lower()
        if 'flask' in code_lower:
            return "Flask"
        if 'django' in code_lower:
            return "Django"
        if 'fastapi' in code_lower:
            return "FastAPI"
        return "Nenhum"

    @staticmethod
    def framework_instructions(framework: str) -> str:
        """Retorna instruções específicas para o framework detectado."""
        instructions = {
            "Flask": """
            - Use @app.route corretamente para registrar rotas.
            - Organize imports: from flask import Flask, render_template, request.
            - Execute com app.run(host='0.0.0.0', port=8080, debug=True).
            """,
            "Django": """
            - Organize em views, models e urls.
            - Cada view deve ser uma função que recebe 'request' como parâmetro.
            - Configure urls.py corretamente.
            """,
            "FastAPI": """
            - Utilize @app.get(), @app.post() para definir rotas.
            - Organize imports: from fastapi import FastAPI, APIRouter, Request.
            - Use uvicorn para rodar o servidor.
            """
        }
        return instructions.get(framework, "")

    @staticmethod
    def enhance_prompt_with_framework(prompt: str, code: str) -> str:
        """Adiciona instruções de framework ao prompt de correção."""
        framework = FrameworkPatterns.detect_framework(code)
        extra = FrameworkPatterns.framework_instructions(framework)
        if extra:
            return prompt.replace("Contexto adicional:", f"Contexto adicional:\n{extra}")
        return prompt
