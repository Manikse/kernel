import os

class FileDriver:
    """
    A Kernel driver that allows agents to interact with the local disk.
    """
    def __init__(self, base_path: str = "./workspace"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def write_file(self, filename: str, content: str):
        path = os.path.join(self.base_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File {filename} written successfully."

    def read_file(self, filename: str) -> str:
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "Error: File not found."