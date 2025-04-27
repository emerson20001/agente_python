# utils/logger.py

def print_info(message: str):
    print(f"\u001b[32m[INFO]\u001b[0m {message}")

def print_warning(message: str):
    print(f"\u001b[33m[WARNING]\u001b[0m {message}")

def print_error(message: str):
    print(f"\u001b[31m[ERROR]\u001b[0m {message}")
