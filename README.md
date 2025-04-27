
# Código Profissional - Correção Automatizada de Projetos

Este projeto é um **agente automático de reestruturação de código**, que analisa todos os arquivos de um projeto, gera correções baseadas em boas práticas profissionais e permite aplicar as melhorias de forma controlada.

## Funcionalidades
- Análise de funções, chamadas e dependências entre arquivos.
- Geração de sugestões de melhorias usando a OpenAI API.
- Backup automático antes de alterações.
- Correção com base no framework detectado (Flask, Django, FastAPI).
- Opção de conversa para tirar dúvidas sobre o código.

## Estrutura Principal
- `main.py` → Inicia o processo.
- `services/` → Serviços auxiliares como scanner, backup, correção.
- `utils/` → Utilitários de logging.
- `config/` → Configurações de ambiente.

## Como usar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure o arquivo `.env` com:
   ```
   OPENAI_API_KEY=sua-chave-da-openai
   OPENAI_MODEL=gpt-4o
   BACKUP_FOLDER=./backups
   EXTENSIONS_VALIDAS=.py
   ```

3. Rode o projeto:
   ```bash
   python main.py
   ```

## Requisitos
- Python 3.9+
- Conta na OpenAI com acesso à API de modelos

## Observações
- O backup dos arquivos corrigidos é salvo automaticamente.
- Suporte nativo para projetos em Python, mas pode ser adaptado para outras linguagens.

---

Feito para desenvolvedores que buscam **código limpo e de alta qualidade**.
