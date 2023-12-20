import argparse
from loguru import logger

from domain.languages import LanguageCode
import service.file_translator as file_translator 
import service.path_renamer as path_renamer
from repository.file_repository import FileRepository
from repository.path_repository import PathRepository

def main():
    logger.remove()
    logger.add(sink="logs/translate_directory.log", level="INFO")
    # parser setup
    parser = argparse.ArgumentParser(description='Translate markdown files')
    parser.add_argument('--replace', action='store_true', help='replace original files')
    parser.add_argument('--language',type=str, default='ja', help='language code to translate to')
    args = parser.parse_args()
    
    # prepare repositories
    path_repository = PathRepository()
    file_repository = FileRepository()
    
    #prepare translator
    translator = file_translator.Translator()
    
    language_code = LanguageCode.from_str(args.language)

    # Translate and replace markdown files
    for file_path in path_repository.read_all():
        save_path = file_path if args.replace else path_renamer.get_renamed_path(file_path, language_code)
        translated_text = translator.translate(file_path, language_code)
        
        file_repository.save(save_path, translated_text)
        
if __name__ == "__main__":
    main()