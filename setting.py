import os
from openai import OpenAI

TRANSLATE_TARGET_FILES_PATH = os.path.join(os.path.dirname(__file__), "file_paths.txt")

CLIENT = OpenAI(api_key=os.environ["OPENAI_API_KEY"])