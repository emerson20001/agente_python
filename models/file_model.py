# models/file_model.py

class CodeFile:
    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content
