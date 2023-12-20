import os, argparse
from dataclasses import dataclass

from extensions import FileExtension
from path_repository import PathRepository

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
            
    @classmethod
    def from_file_ext_strs(cls, ext_strs: list[str]) -> "PathRetriever":
        file_extensions = list(map(FileExtension.from_str, ext_strs))
        return PathRetriever(file_extensions)
        
def main():
    parser = argparse.ArgumentParser(description='Extract files from a directory')
    parser.add_argument('--directory',type=str, help='directory to extract files from')
    parser.add_argument('--extensions', nargs='+', type=str, default=['.md'], help='file extensions to extract')
    args = parser.parse_args()
    
    retriever = PathRetriever.from_file_ext_strs(args.extensions)
    
    path_list = retriever.retrieve(args.directory)
    PathRepository().write(path_list)
    
if __name__ == "__main__":
    main()