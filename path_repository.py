import setting

class PathRepository:
    
    def read_all(self) -> list[str]:
        with open(setting.TRANSLATE_TARGET_FILES_PATH, "r") as file:
            return file.read().splitlines()
        
    def write(self, path_list: list[str]):
        with open(setting.TRANSLATE_TARGET_FILES_PATH, "w") as file:
            file.write("\n".join(path_list))