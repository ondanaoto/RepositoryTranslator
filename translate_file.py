import os
from openai import OpenAI
import argparse
from constants import LanguageCode, FileExtension, str_to_language_code, str_to_file_extension

LAST_CHARACTERS = 100

def translate_text(text, file_extension: FileExtension, dst_language_code: LanguageCode, client= OpenAI()):
    prompt = f"Please translate the following {str(file_extension)} file into {str(dst_language_code)}. In cases where the document is lengthy, it's not necessary to forcibly summarize the entire content. If the translation needs to be cut short due to the document's length, that's perfectly fine. \n\nFile content:\n{text}"
    response_texts = []
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": prompt}
        ]
    )
    response_texts = response.choices[0].message.content
    # if the completion stop by max_tokens, we need to continue the completion
    if response.choices[0].finish_reason == "length":
        continuing_prompt = f"I would like to have the following `{str(file_extension)}` file translated into {str(dst_language_code)}. Fortunately, it has already been partially translated, and I will provide the last 100 charecters of the translation that has been completed. Please continue translating from where it left off so that the translations are smoothly connected. In cases where the document is lengthy, it's not necessary to forcibly summarize the entire content. In cases where the document is lengthy, it's not necessary to forcibly summarize the entire content. If the translation needs to be cut short due to the document's length, that's perfectly fine.\n\nFile: {text}\n\nLast {LAST_CHARACTERS} characters:{response_texts[-LAST_CHARACTERS:]}"
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a translator."},
                {"role": "user", "content": continuing_prompt}
            ]
        )
        response_texts += response.choices[0].message.content
        
    return response_texts

def translate_and_save_file(src_file_path, dst_language_code: LanguageCode, client= OpenAI(), replace=False):
    extension = str_to_file_extension(os.path.splitext(src_file_path)[1])
    print(f"Translating {src_file_path} to {str(dst_language_code)}...", end="")
    
    with open(src_file_path, "r") as file:
        content = file.read()
    
    translated_text = translate_text(content, extension, dst_language_code, client=client)
    print("Done!")

    # Save the translated content to a new file
    file_base = os.path.splitext(src_file_path)[0]
    dst_file_path = f"{file_base}_{dst_language_code.value}{extension.value}"
    
    if replace:
        dst_file_path = src_file_path
        
    print(f"Saving translated file to {dst_file_path}...", end="")
    with open(dst_file_path, "w") as translated_file:
        translated_file.write(translated_text)
        print("Done!")

def main():
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
        dst_language_code=str_to_language_code(args.language), \
        client=client, \
        replace=args.replace
    )
    
if __name__ == "__main__":
    main()