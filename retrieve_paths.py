import argparse
from repository.path_repository import PathRepository
from service.paths_retriever import PathRetriever

def main():
    parser = argparse.ArgumentParser(description='Extract files from a directory')
    parser.add_argument('--directory',type=str, help='directory to extract files from')
    parser.add_argument('--extensions', nargs='+', type=str, default=['.md'], help='file extensions to extract')
    args = parser.parse_args()
    
    path_repository = PathRepository()
    retriever = PathRetriever.from_file_ext_strs(args.extensions)
    
    path_list = retriever.retrieve(args.directory)
    path_repository.write(path_list)
    
if __name__ == "__main__":
    main()