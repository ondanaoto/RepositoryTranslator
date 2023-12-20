import os
import sys
import argparse
from openai import OpenAI
from loguru import logger

import languages as lang
from translate_file import translate_and_save_file

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    # parser setup
    parser = argparse.ArgumentParser(description='Translate markdown files')
    parser.add_argument('--replace', action='store_true', help='replace original files')
    parser.add_argument('--language',type=str, default='ja', help='language code to translate to')
    args = parser.parse_args()
    
    # set up OpenAI client
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    # fetch target file paths
    with open("file_paths.txt", "r") as file:
        target_file_paths = file.read().splitlines()

    # Translate and replace markdown files
    for file_path in target_file_paths:
        translate_and_save_file(
            file_path, \
            dst_language_code=lang.parse_language_code(args.language), \
            client=client, \
            replace=args.replace
        )
        
if __name__ == "__main__":
    main()