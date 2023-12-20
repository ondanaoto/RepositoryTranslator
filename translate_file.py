import os
import sys
from loguru import logger
from openai import OpenAI
import argparse

import languages as lang
import extensions as ext

LAST_CHARACTERS = 100

def translate_segment(text, file_extension: ext.FileExtension, dst_language_code: lang.LanguageCode, client= OpenAI()):
    prompt = f"In cases where the document is lengthy, it's not necessary to forcibly summarize the entire content. If the translation needs to be cut short due to the document's length, that's perfectly fine. Please translate the following {str(file_extension)} file into {str(dst_language_code)} and return only the translation content. \n\nFile content:\n{text}"
    response_texts = []
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": f"You are a perfect translator who translates {str(file_extension)} files into {str(dst_language_code)}."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    response_texts = response.choices[0].message.content
        
    return response_texts

def split_text(text, max_tokens=1024) -> list[str]:
    segments = []
    current_segment = ""
    current_length = 0

    for sentence in text.split('\n\n'):
        sentence += '\n\n'
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_tokens:
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
        logger.debug(f"Each segment first 100 tokens: {segment.split()[:100]}")
    return segments

def translate(text, file_extension: ext.FileExtension, dst_language_code: lang.LanguageCode, client= OpenAI()):
    segments = split_text(text)
    translated_segments = []
    for segment in segments:
        translated_segments.append(translate_segment(segment, file_extension, dst_language_code, client=client))
    return "\n\n".join(translated_segments)

def translate_and_save_file(src_file_path, dst_language_code: lang.LanguageCode, client= OpenAI(), replace=False):
    extension = ext.parse(os.path.splitext(src_file_path)[1])
    logger.info(f"Translating {src_file_path} to {str(dst_language_code)} ...", end="")
    
    with open(src_file_path, "r") as file:
        content = file.read()
    
    translated_text = translate(content, extension, dst_language_code, client=client)
    logger.info("Done!")

    # Save the translated content to a new file
    file_base = os.path.splitext(src_file_path)[0]
    dst_file_path = f"{file_base}_{dst_language_code.value}{extension.value}"
    
    if replace:
        dst_file_path = src_file_path
        
    with open(dst_file_path, "w") as translated_file:
        translated_file.write(translated_text)

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    # parser setup
    parser = argparse.ArgumentParser(description='Translate markdown files')
    parser.add_argument('--file',type=str, help='file path to translate')
    parser.add_argument('--language',type=str, default='ja', help='language code to translate to')
    parser.add_argument('--replace', action='store_true', help='replace original files')
    args = parser.parse_args()
    
    # set up OpenAI client
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # Translate and replace files
    translate_and_save_file(
        src_file_path=args.file, \
        dst_language_code=lang.parse(args.language), \
        client=client, \
        replace=args.replace
    )
    
def debug():
    logger.remove()
    logger.add(sys.stderr, level="DEBUG", sink="debug.log")
    # parser setup
    parser = argparse.ArgumentParser(description='Translate markdown files')
    parser.add_argument('--file',type=str, help='file path to translate')
    parser.add_argument('--language',type=str, default='ja', help='language code to translate to')
    parser.add_argument('--replace', action='store_true', help='replace original files')
    args = parser.parse_args()
    
    with open(args.file, "r") as file:
        content = file.read()
    
    split_text(content)
    
if __name__ == "__main__":
    main()