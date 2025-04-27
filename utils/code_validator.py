# utils/validator.py

import re

def validar_blocos_codigo_PRO(conteudo: str) -> dict:
    """
    Valida abertura e fechamento de blocos { } dentro de PHP:
    - class
    - function
    - if/else/elseif
    - foreach/for/while
    - try/catch/finally
    Ignora HTML e arrays [ ].
    """

    padroes_blocos = [
        r"\bclass\b",
        r"\bfunction\b",
        r"\bif\b",
        r"\belseif\b",
        r"\belse\b",
        r"\bforeach\b",
        r"\bfor\b",
        r"\bwhile\b",
        r"\btry\b",
        r"\bcatch\b",
        r"\bfinally\b",
    ]

    total_abertos = 0
    total_fechados = 0
    inconsistencias = []
    pilha_blocos = []

    dentro_php = False
    linhas = conteudo.splitlines()

    for numero_linha, linha in enumerate(linhas, start=1):
        linha_limpa = linha.strip()

        if '<?php' in linha_limpa:
            dentro_php = True
        if '?>' in linha_limpa:
            dentro_php = False
            continue

        if not dentro_php:
            continue  # Ignorar qualquer coisa fora do PHP

        # Ignorar linhas de array simples: ['...', '...']
        if linha_limpa.startswith('[') and linha_limpa.endswith(']'):
            continue

        # Detecta início de bloco
        for padrao in padroes_blocos:
            if re.search(padrao, linha_limpa) and '{' in linha_limpa:
                pilha_blocos.append((linha_limpa, numero_linha))
                total_abertos += 1
                break

        # Abertura manual de bloco
        if linha_limpa == '{':
            pilha_blocos.append(('{', numero_linha))
            total_abertos += 1

        # Fechamento de bloco
        if '}' in linha_limpa:
            if pilha_blocos:
                pilha_blocos.pop()
                total_fechados += 1
            else:
                inconsistencias.append(f"Chave '}}' inesperada na linha {numero_linha}")

    # Se sobraram blocos abertos
    for bloco, linha in pilha_blocos:
        inconsistencias.append(f"Bloco aberto sem fechamento iniciado na linha {linha}: {bloco}")

    return {
        "total_abertos": total_abertos,
        "total_fechados": total_fechados,
        "inconsistencias": inconsistencias
    }
