# main.py

import os
from services.file_scanner import FileScanner
from services.project_analyzer import ProjectAnalyzer
from services.openai_client import OpenAIClient
from services.backup_service import BackupService
from services.correction_planner import CorrectionPlanner
from utils.logger import print_info, print_warning, print_error
from utils.api_validator import validar_openai_api_key
from utils.code_validator import validar_blocos_codigo_PRO
from config.config import OPENAI_API_KEY

def detect_language(text: str) -> str:
    languages = ['python', 'java', 'javascript', 'typescript', 'php', 'c#', 'c++', 'ruby', 'go', 'swift']
    text = text.lower()
    for lang in languages:
        if lang in text:
            return lang.capitalize()
    return "Python"

def detect_interaction_type(text: str) -> str:
    return "conversa" if "?" in text else "correcao"

def detectar_linguagem_arquivo(filepath: str) -> str:
    if filepath.endswith(".py"):
        return "Python"
    elif filepath.endswith(".php"):
        return "PHP"
    elif filepath.endswith(".js"):
        return "JavaScript"
    elif filepath.endswith(".ts"):
        return "TypeScript"
    elif filepath.endswith(".java"):
        return "Java"
    else:
        return "Desconhecido"

def gerar_contexto_por_linguagem(linguagem: str) -> str:
    instrucoes_gerais = (
        "- Corrija apenas erros reais de sintaxe sem alterar o estilo.\n"
        "- Preserve a estrutura, indentação e organização original do código.\n"
        "- Não reformatar o código. Não quebrar linhas existentes.\n"
        "- Complete funções, métodos ou classes incompletas.\n"
        "- Deixe o código funcional.\n"
    )

    if linguagem == "Python":
        return instrucoes_gerais + "- Aplique PEP8 apenas se não alterar a estrutura.\n"
    elif linguagem == "PHP":
        try:
            with open("context_php.txt", "r", encoding="utf-8") as f:
                contexto_php = f.read()
            return instrucoes_gerais + contexto_php
        except Exception as e:
            print_warning(f"Não foi possível carregar o contexto PHP: {e}")
            return instrucoes_gerais
    elif linguagem == "JavaScript":
        return instrucoes_gerais + "- Use ES6 onde aplicável sem mudar a organização.\n"
    elif linguagem == "TypeScript":
        return instrucoes_gerais + "- Tipifique variáveis e funções corretamente sem reformatar.\n"
    elif linguagem == "Java":
        return instrucoes_gerais + "- Aplique JavaBeans e SOLID respeitando a estrutura existente.\n"
    else:
        return instrucoes_gerais

def read_project_structure(files: list) -> None:
    print_info("\nEstrutura do projeto:")
    structure = {}
    for file in files:
        folder = os.path.dirname(file.path)
        structure.setdefault(folder, []).append(os.path.basename(file.path))

    for folder, filenames in structure.items():
        print_info(f"Pasta: {folder}")
        for filename in filenames:
            print_info(f"  - {filename}")

def validar_blocos_codigo_local(file) -> bool:
    """Executa a validação de blocos abertos/fechados no arquivo."""
    resultado = validar_blocos_codigo_PRO(file.content)
    if resultado["inconsistencias"]:
        print_warning(f"\n⚠️ Inconsistências encontradas no arquivo {file.path}:")
        for erro in resultado["inconsistencias"]:
            print_warning(f"- {erro}")
        return False
    else:
        print_info(f"✅ Estrutura de blocos validada com sucesso em {file.path}.")
        return True

def process_file(file, planner, openai_client, backup_service, global_context, default_language):
    filepath = file.path
    filename = os.path.basename(filepath)

    linguagem_detectada = detectar_linguagem_arquivo(filepath)
    language_to_use = linguagem_detectada if linguagem_detectada != "Desconhecido" else default_language

    print_info(f"\nAnalisando: {filepath} (linguagem: {language_to_use})")

    if not validar_blocos_codigo_local(file):
        print_warning("⚠️ Correção manual necessária antes de prosseguir.\n")
        return

    context_base = planner.generate_context_for_file(filename)
    contexto_de_boas_praticas = gerar_contexto_por_linguagem(language_to_use)
    backup_service.backup_file(filepath)
    interaction_type = detect_interaction_type(global_context)

    suggestion = openai_client.get_suggestion(
        file.content,
        extra_context=(
            "- Corrija apenas onde houver erro de sintaxe.\n"
            "- Mantenha o estilo atual do arquivo.\n"
            "- Não mude espaçamento, indentação ou formatação se estiver correto.\n"
        ) + context_base + global_context + "\n" + contexto_de_boas_praticas,
        language=language_to_use,
        mode=interaction_type
    )

    if not suggestion:
        print_warning("Nenhuma sugestão gerada para este arquivo.")
        return

    print("\nSugestão recebida:")
    print("=" * 80)
    print(suggestion)
    print("=" * 80)

    while True:
        choice = input("\nAplicar esta correção? (s = sim / n = não / t = novo comando): ").strip().lower()

        if choice == 's':
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(suggestion)
                print_info(f"✅ Arquivo sobrescrito com sucesso: {filepath}")
            except Exception as e:
                print_error(f"❌ Erro ao salvar {filepath}: {e}")
            break

        elif choice == 'n':
            print_warning("⚠️ Correção ignorada.")
            break

        elif choice == 't':
            new_text = input("\nDigite novo comando para o GPT:\n").strip()
            if new_text:
                new_language = detect_language(new_text)
                interaction_type = detect_interaction_type(new_text)
                global_context += f"\n- {new_text}"

                suggestion = openai_client.get_suggestion(
                    file.content,
                    extra_context=context_base + global_context + "\n" + contexto_de_boas_praticas,
                    language=new_language,
                    mode=interaction_type
                )

                if suggestion:
                    print("\nNova sugestão gerada:")
                    print("=" * 80)
                    print(suggestion)
                    print("=" * 80)
                else:
                    print_error("❌ Falha ao gerar nova sugestão.")
            else:
                print_warning("Nenhuma instrução adicional fornecida.")
        else:
            print_warning("Opção inválida. Digite 's', 'n' ou 't'.")

def main():
    print_info("\n🚀 Agente Profissional de Correção de Código 🚀")

    if not validar_openai_api_key(OPENAI_API_KEY):
        print_error("\n❌ Chave de API inválida. Encerrando execução.")
        exit(1)

    folder_path = input("\nDigite o caminho da pasta do projeto: ").strip()

    scanner = FileScanner(folder_path)
    files = scanner.scan_all_files()

    if not files:
        print_error("\nNenhum arquivo encontrado!")
        return

    read_project_structure(files)
    print_info("\nTodos os arquivos lidos com sucesso.")

    analyzer = ProjectAnalyzer()
    for file in files:
        linguagem_detectada = detectar_linguagem_arquivo(file.path)
        if linguagem_detectada == "Python":
            analyzer.analyze_file(file.content, os.path.basename(file.path))

    planner = CorrectionPlanner(analyzer)
    openai_client = OpenAIClient()
    backup_service = BackupService()

    global_context = ""
    language = "Python"

    extra_instruction = input("\nDeseja adicionar alguma instrução extra? (Enter para pular): ").strip()
    if extra_instruction:
        language = detect_language(extra_instruction)
        global_context += f"\n- {extra_instruction}"

    for file in files:
        process_file(file, planner, openai_client, backup_service, global_context, language)

    print_info("\n✅ Processo de análise concluído!")

if __name__ == "__main__":
    main()
