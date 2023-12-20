import os
from languages import LanguageCode

def get_renamed_path(path: str, language_code: LanguageCode) -> str:
    root, ext = os.path.splitext(path)
    return f"{root}_{language_code}{ext}"