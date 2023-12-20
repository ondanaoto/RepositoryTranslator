import os
from typing import Any
from loguru import logger

from domain.languages import LanguageCode
from domain.extensions import FileExtension
from repository.file_repository import FileRepository
from domain.professors import LLMFileTranslator

class Translator:
    
    SEGMENT_LENGTH_LIMIT = 1024
    SPLIT_SYMBOL = "\n\n"
    file_repository = FileRepository()
    llm_file_translator = LLMFileTranslator()
    
    def translate(self, file_path: str, language_code: LanguageCode) -> str:
        segments = []
        for context in self._get_contexts(file_path, language_code):
            segment = self.llm_file_translator.response(context)
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
    
    def _get_file_ext(self, file_path: str) -> FileExtension:
        return FileExtension.from_str(os.path.splitext(file_path)[1])
    
    def _get_contexts(self, file_path: str, language_code: LanguageCode) -> list[dict[str, Any]]:
        file_ext = self._get_file_ext(file_path)
        raw_text = self.file_repository.load(file_path)
        split_texts = self._split_text(raw_text)
        return [
            {
                "file_extension": file_ext,
                "target_language_code": language_code,
                "raw_text": text
            }
            for text in split_texts
        ]