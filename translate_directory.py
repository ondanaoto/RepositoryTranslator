import os
import sys
import argparse
from openai import OpenAI
from loguru import logger

from languages import LanguageCode
import translate_file 
import rename_path
from file_repository import FileRepository
from path_repository import PathRepository

def main():
    # parser setup
    parser = argparse.ArgumentParser(description='Translate markdown files')
    parser.add_argument('--replace', action='store_true', help='replace original files')
    parser.add_argument('--language',type=str, default='ja', help='language code to translate to')
    args = parser.parse_args()
    
    # prepare repositories
    path_repository = PathRepository()
    file_repository = FileRepository()
    
    #prepare translator
    translator = translate_file.Translator()
    
    language_code = LanguageCode.from_str(args.language)

    # Translate and replace markdown files
    for file_path in path_repository.read_all():
        save_path = file_path if args.replace else rename_path.get_renamed_path(file_path, language_code)
        translated_text = translator.translate(file_path, language_code)
        
        file_repository.save(save_path, translated_text)
        
if __name__ == "__main__":
    main()