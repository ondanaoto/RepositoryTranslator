import os, argparse
from typing import List

import extensions as ext

def extract_file_paths(directory, file_extension_list: List[ext.FileExtension]) -> None:
    file_path_list = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if any(file.endswith(ext.value) for ext in file_extension_list)
    ]
    with open("file_paths.txt", "w") as file:
        file.write("\n".join(file_path_list))
        
def main():
    parser = argparse.ArgumentParser(description='Extract files from a directory')
    parser.add_argument('--directory',type=str, help='directory to extract files from')
    parser.add_argument('--extensions', nargs='+', type=str, default=['.md'], help='file extensions to extract')
    args = parser.parse_args()
    
    file_extensions = list(map(ext.parse_file_extension, args.extensions))
    
    extract_file_paths(args.directory, file_extensions)
    
if __name__ == "__main__":
    main()