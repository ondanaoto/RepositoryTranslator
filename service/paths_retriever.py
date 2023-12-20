import os
from dataclasses import dataclass

from domain.extensions import FileExtension

@dataclass(frozen=True)
class PathRetriever:
    
    target_file_exts: list[FileExtension]
    
    def retrieve(self, dir: str) -> list[str]:
        file_path_list = [
            os.path.join(root, file)
            for root, _, files in os.walk(dir)
            for file in files
            if any(file.endswith(ext.value) for ext in self.target_file_exts)
        ]
        
        return file_path_list