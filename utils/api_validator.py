# utils/api_validator.py

import requests

def validar_openai_api_key(api_key: str) -> bool:
    """Testa se a chave da OpenAI é válida com uma requisição simples."""
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            print("\n A chave da OpenAI é inválida ou expirou.")
            print(" Gere uma nova chave em: https://platform.openai.com/account/api-keys")
        else:
            print(f"\n Erro ao validar a chave: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\n Erro de conexão ao validar a chave: {e}")
    
    return False
