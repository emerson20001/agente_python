# services/validator.py

import ast
from utils.logger import print_error

def is_function_present(code: str, function_name: str) -> bool:
    """Verifica se uma função específica existe no código."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return True
        return False
    except Exception as e:
        print_error(f"Erro ao validar funções: {e}")
        return False
