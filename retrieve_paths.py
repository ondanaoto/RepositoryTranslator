import os, argparse
from typing import List
from dataclasses import dataclass

from extensions import FileExtension

@dataclass(frozen=True)
class PathRetriever:
    
    target_file_exts: List[FileExtension]
    
    def retrieve(self, directory: str) -> None:
        file_path_list = [
            os.path.join(root, file)
            for root, _, files in os.walk(directory)
            for file in files
            if any(file.endswith(ext.value) for ext in self.target_file_exts)
        ]
        with open("file_paths.txt", "w") as file:
            file.write("\n".join(file_path_list))
            
    @classmethod
    def from_file_ext_strs(cls, ext_strs: List[str]) -> "PathRetriever":
        file_extensions = list(map(FileExtension.from_str, ext_strs))
        return PathRetriever(file_extensions)
        
def main():
    parser = argparse.ArgumentParser(description='Extract files from a directory')
    parser.add_argument('--directory',type=str, help='directory to extract files from')
    parser.add_argument('--extensions', nargs='+', type=str, default=['.md'], help='file extensions to extract')
    args = parser.parse_args()
    
    retriever = PathRetriever.from_file_ext_strs(args.extensions)
    retriever.retrieve(args.directory)
    
if __name__ == "__main__":
    main()