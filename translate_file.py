import os
import sys
from typing import Any
from dataclasses import dataclass
from loguru import logger
from openai import OpenAI
import argparse

from languages import LanguageCode
from extensions import FileExtension
from file_repository import FileRepository
from professors import LLMFileTranslator
import rename_path

class Translator:
    
    SEGMENT_LENGTH_LIMIT = 1024
    SPLIT_SYMBOL = "\n\n"
    
    def translate(self, file_path: str, language_code: LanguageCode) -> str:
        segments = []
        for context in self._get_contexts(file_path, language_code):
            segment = LLMFileTranslator().response(context)
            segments.append(segment)

        return self.SPLIT_SYMBOL.join(segments)
    
    def _split_text(self, text: str) -> list[str]:
        segments = []
        current_segment = ""
        current_length = 0

        for sentence in text.split('\n\n'):
            sentence += '\n\n'
            sentence_length = len(sentence.split())
            if current_length + sentence_length > self.SEGMENT_LENGTH_LIMIT:
                segments.append(current_segment.strip())
                current_segment = sentence
                current_length = sentence_length
            else:
                current_segment += " " + sentence
                current_length += sentence_length

        if current_segment:
            segments.append(current_segment.strip())
            
        logger.debug(f"Number of segments: {len(segments)}")
        for segment in segments:
            logger.debug(f"Each segment token size: {len(segment.split())}")
            debug_token_size = 100
            logger.debug(f"Each segment first {debug_token_size} tokens: {segment.split()[:debug_token_size]}")
        return segments
    
    def _get_file_ext(file_path: str) -> FileExtension:
        return FileExtension.from_str(os.path.splitext(file_path)[1])
    
    def _get_contexts(self, file_path: str, language_code: LanguageCode) -> list[dict[str, Any]]:
        file_ext = self._get_file_ext(file_path)
        raw_text = FileRepository.load(file_path)
        split_texts = self._split_text(raw_text)
        return [
            {
                "file_extension": file_ext,
                "target_language_code": language_code,
                "raw_text": text
            }
            for text in split_texts
        ]

def main():
    # parser setup
    parser = argparse.ArgumentParser(description='Translate markdown files')
    parser.add_argument('--file',type=str, help='file path to translate')
    parser.add_argument('--language',type=str, default='ja', help='language code to translate to')
    parser.add_argument('--replace', action='store_true', help='replace original files')
    args = parser.parse_args()
    
    translator = Translator()
    fileRepository  = FileRepository()
    language_code = LanguageCode.from_str(args.language)
    
    save_path = args.file if args.replace else rename_path.get_renamed_path(args.file, language_code)
    
    fileRepository.save(
        save_path,
        translator.translate(save_path, language_code)
    )
    
if __name__ == "__main__":
    main()