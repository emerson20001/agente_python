# main.py

from services.file_scanner import FileScanner
from services.project_analyzer import ProjectAnalyzer
from services.openai_client import OpenAIClient
from services.backup_service import BackupService
from services.correction_planner import CorrectionPlanner
from utils.logger import print_info, print_warning, print_error
import os

def detect_language(text: str) -> str:
    """Detecta linguagem-alvo com base no texto."""
    languages = ['python', 'java', 'javascript', 'typescript', 'php', 'c#', 'c++', 'ruby', 'go', 'swift']
    text = text.lower()
    for lang in languages:
        if lang in text:
            return lang.capitalize()
    return "Python"

def detect_interaction_type(text: str) -> str:
    """Determina se o usuário quer correção ou conversa."""
    return "conversa" if "?" in text else "correcao"

def read_project_structure(files: list) -> None:
    """Imprime estrutura de pastas e arquivos encontrados."""
    print_info(" Estrutura do projeto encontrada:")
    structure = {}
    for file in files:
        folder = os.path.dirname(file.path)
        structure.setdefault(folder, []).append(os.path.basename(file.path))

    for folder, filenames in structure.items():
        print_info(f"Pasta: {folder}")
        for filename in filenames:
            print_info(f"  - {filename}")

def process_file(file, planner, openai_client, backup_service, global_context, language):
    """Processa a correção de um único arquivo."""
    filepath = file.path
    filename = os.path.basename(filepath)

    print_info(f"\nAnalisando arquivo: {filepath}")

    context_base = planner.generate_context_for_file(filename)
    backup_service.backup_file(filepath)
    interaction_type = detect_interaction_type(global_context)

    suggestion = openai_client.get_suggestion(
        file.content,
        extra_context=context_base + global_context,
        language=language,
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
        choice = input("\nDeseja aplicar esta correção? (s = sim / n = não / t = novo texto para o projeto): ").strip().lower()

        if choice == 's':
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(suggestion)
                print_info(f"Arquivo sobrescrito: {filepath}")
            except Exception as e:
                print_error(f"Erro ao sobrescrever {filepath}: {e}")
            break

        elif choice == 'n':
            print_warning("Correção ignorada.")
            break

        elif choice == 't':
            new_text = input("\nDigite novo comando para o GPT:\n").strip()
            if new_text:
                new_language = detect_language(new_text)
                interaction_type = detect_interaction_type(new_text)
                global_context += f"\n- {new_text}"

                if interaction_type == "conversa":
                    print_info(" Modo conversa detectado.")
                    answer = openai_client.get_suggestion(
                        file.content,
                        extra_context=context_base + global_context,
                        language=new_language,
                        mode="conversa"
                    )
                    if answer:
                        print("\nResposta da conversa:")
                        print("=" * 80)
                        print(answer)
                        print("=" * 80)
                    else:
                        print_error("Falha ao obter resposta de conversa.")
                    continue  # Volta para o loop perguntando novamente

                # Se for nova correção, reenvia
                suggestion = openai_client.get_suggestion(
                    file.content,
                    extra_context=context_base + global_context,
                    language=new_language,
                    mode="correcao"
                )

                if suggestion:
                    print("\nNova sugestão de correção:")
                    print("=" * 80)
                    print(suggestion)
                    print("=" * 80)
                else:
                    print_error("Falha ao gerar nova sugestão.")

            else:
                print_warning("Nenhum comando fornecido.")
        else:
            print_warning("Opção inválida. Digite 's', 'n' ou 't'.")

def main():
    print_info("\n Agente Profissional de Correção de Código ")

    folder_path = input("\nDigite o caminho completo da pasta do projeto: ").strip()

    scanner = FileScanner(folder_path)
    files = scanner.scan_all_files()

    if not files:
        print_error("\nNenhum arquivo encontrado!")
        return

    read_project_structure(files)
    print_info("\n Todos os arquivos lidos.")

    analyzer = ProjectAnalyzer()
    for file in files:
        analyzer.analyze_file(file.content, os.path.basename(file.path))

    planner = CorrectionPlanner(analyzer)
    openai_client = OpenAIClient()
    backup_service = BackupService()

    global_context = ""
    language = "Python"

    extra_instruction = input("\nDeseja adicionar alguma instrução inicial? (Enter para pular): ").strip()
    if extra_instruction:
        language = detect_language(extra_instruction)
        global_context += f"\n- {extra_instruction}"

    for file in files:
        process_file(file, planner, openai_client, backup_service, global_context, language)

    print_info("\n Processo concluído!\n")

if __name__ == "__main__":
    main()
