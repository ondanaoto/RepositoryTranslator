class FileRepository:

    def save(self, file_path: str, data: str, mode='w') -> None:
        with open(file_path, mode) as f:
            f.write(data)

    def load(self, file_path: str) -> str:
        with open(file_path, 'r') as f:
            return f.read()