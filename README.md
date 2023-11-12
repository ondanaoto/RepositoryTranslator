# Repository Translator

Repository Translator is a tool designed to translate files within a specific directory and save the results. This tool performs file extraction, translation, and saving of the translated files.

## Modules

### 1. retrieve_paths.py

#### Purpose
To retrieve paths of all files with specified file extensions within a directory and list them in `file_paths.txt`.

#### Usage
Run the following command from the command line:

```
python retrieve_paths.py --directory [Target Directory] --extensions [File Extensions to Extract]
```

Example:

```
python retrieve_paths.py --directory ./my_folder --extensions .md .txt
```

### 2. translate_file.py

#### Purpose
To translate a specified file into a designated language and save the translated content in the same directory.

#### Usage
Run the following command from the command line:

```
python translate_file.py --file [Path to File to Translate] --language [Target Language Code] --replace
```

Example:

```
python translate_file.py --file ./my_folder/document.md --language ja --replace
```

### 3. translate_directory.py

#### Purpose
To translate all files listed in `file_paths.txt` into a specified language.

#### Usage
Run the following command from the command line:

```
python translate_directory.py --language [Target Language Code] --replace
```

Example:

```
python translate_directory.py --language ja --replace
```

## Important Notes

- This tool uses the **OpenAI API**. An API key is required to use the API, and charges may apply depending on the usage.
- After running `retrieve_paths.py`, please check the file paths listed in `file_paths.txt`. If there are any files you do not wish to translate, remove them from the list before running `translate_directory.py`.
- The `--replace` option will overwrite the original files with the translated content. Use this option with caution.

## License

This project is released under the [MIT license](LICENSE).