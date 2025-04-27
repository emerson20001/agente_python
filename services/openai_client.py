# services/openai_client.py

import requests
import json
import ast
import re
from services.framework_patterns import FrameworkPatterns
from config.config import OPENAI_API_KEY, OPENAI_MODEL
from utils.logger import print_info, print_warning, print_error

class OpenAIClient:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.url = "https://api.openai.com/v1/chat/completions"

    def sanitize_response(self, response: str) -> str:
        """Limpa a resposta, removendo markdown e mantendo apenas código."""
        if response.startswith("```"):
            lines = response.splitlines()
            lines = lines[1:] if lines and lines[0].startswith("```") else lines
            lines = lines[:-1] if lines and lines[-1].startswith("```") else lines
            response = "\n".join(lines)

        filtered = []
        for line in response.splitlines():
            if line.strip() and (
                line.strip().startswith("#") 
                or line.strip().startswith("@") 
                or re.match(r"^[a-zA-Z0-9_()\[\]\{\}\s\+\-\*/=<>.:,'\"\\]", line.strip())
            ):filtered.append(line)


        return "\n".join(filtered).strip()

    def validate_python_code(self, code: str) -> bool:
        """Verifica se o código é um Python válido."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def get_prompt(self, code: str, linguagem_destino: str = "Python", contexto_dependencias: str = "") -> str:
        prompt_base = f"""
        Você é um engenheiro de software extremamente qualificado em {linguagem_destino}.

        Seu objetivo é corrigir, reestruturar e aplicar boas práticas profissionais no código fornecido.

        Instruções obrigatórias:

        - Corrija todos os erros de sintaxe, organização, estilo e lógica.
        - Reestruture o código para seguir os padrões corretos de design e arquitetura adequados para a linguagem e framework usado.
        - Se detectar o uso de frameworks (como Flask, Django ou FastAPI):
            - Reconstrua as rotas corretamente usando decorators (@app.route, etc.).
            - Configure corretamente o servidor de desenvolvimento.
            - Organize corretamente os imports necessários.
        - Adapte nomes de funções, variáveis e estruturas de dados para torná-los mais claros e semânticos.
        - Separe responsabilidades em funções pequenas e específicas, se necessário.
        - Aplique sempre boas práticas como:
            - Organização correta dos imports,
            - Separação de responsabilidades,
            - Clareza e semântica nos nomes,
            - Uso correto de decorators,
            - Estrutura consistente e limpa do app.

        Diretrizes finais:

        - Reescreva o código diretamente, sem explicações.
        - NÃO adicione comentários explicativos fora do código.
        - NÃO adicione resumos, análises, listas ou observações após o código.
        - NÃO adicione texto adicional — apenas entregue o novo código completo e pronto para uso.
        - Entregue apenas o código reestruturado, sem mensagens extras.

        Contexto adicional:

        {contexto_dependencias}

        Código para análise:

        {code}
        """
        return prompt_base



    def get_explanation_prompt(self, code: str, extra_context: str = "") -> str:
        """Monta o prompt para perguntas rápidas sobre o código."""
        return f"""
        Você é um assistente de programação.

        Responda de forma curta e direta:

        {extra_context}

        Código:

        {code}
        """

    def get_suggestion(self, code: str, extra_context: str = "", language: str = "Python", mode: str = "correcao") -> str | None:
        """Faz requisição para a API da OpenAI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = (
            self.get_prompt(code, language, extra_context)
            if mode == "correcao"
            else self.get_explanation_prompt(code, extra_context)
        )

        all_responses = ""
        retry = False

        for _ in range(3):
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }

            try:
                response = requests.post(self.url, headers=headers, json=payload)

                if response.status_code == 200:
                    raw = response.json()["choices"][0]["message"]["content"]
                    clean = self.sanitize_response(raw)
                    all_responses += clean.strip()

                    if any(kw in clean.lower() for kw in ["continua", "continuar", "[continua]"]):
                        retry = True
                        prompt = "Continue a resposta anterior sem repetir o que já foi enviado."
                        print_warning("Resposta incompleta. Solicitando continuação...")
                        continue
                    break

                elif response.status_code == 401:
                    print_error("API Key inválida.")
                    return None

                elif response.status_code == 429:
                    print_error("Limite de requisições excedido.")
                    return None

                else:
                    error_message = response.json().get('error', {}).get('message', 'Erro desconhecido')
                    print_error(f"Erro da OpenAI ({response.status_code}): {error_message}")
                    return None

            except requests.exceptions.RequestException as e:
                print_error(f"Erro de conexão com a OpenAI: {e}")
                return None

        if retry:
            print_warning("A resposta pode ainda estar incompleta.")

        return all_responses if all_responses else None
