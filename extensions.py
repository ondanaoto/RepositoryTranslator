from enum import Enum, unique

@unique
class FileExtension(Enum):
    MARKDOWN = '.md'
    TEX = '.tex'
    HTML = '.html'
    XML = '.xml'
    DOC = '.doc'
    DOCX = '.docx'
    JS = '.js'
    TS = '.ts'
    JSX = '.jsx'
    JSON = '.json'
    
    def __str__(self):
        return self.value

def parse_file_extension(input_str) -> FileExtension:
    for ext in FileExtension:
        if ext.value == input_str:
            return ext
    raise ValueError(f"No matching enum for string: {input_str}")