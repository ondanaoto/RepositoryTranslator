import argparse
from domain.extensions import FileExtension
from repository.path_repository import PathRepository
from service.paths_retriever import PathRetriever

def main():
    parser = argparse.ArgumentParser(description='Extract files from a directory')
    parser.add_argument('--directory',type=str, help='directory to extract files from')
    parser.add_argument('--extensions', nargs='+', type=str, default=['.md'], help='file extensions to extract')
    args = parser.parse_args()
    
    file_exts = list(map(FileExtension.from_str, args.extensions))
    
    path_repository = PathRepository()
    retriever = PathRetriever(file_exts)
    
    path_list = retriever.retrieve(args.directory)
    path_repository.write(path_list)
    
if __name__ == "__main__":
    main()