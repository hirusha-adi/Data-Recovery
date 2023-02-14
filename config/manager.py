import os
import typing as t

class ModuleManager:
    def __init__(self, module_name:str) -> None:
        self.module_name = module_name
    
    def mprint(self, *args) -> None:
        print("[{}]".format(self.module_name), *args)
    
    def merror(self, *args) -> None:
        print("[{}]".format(self.module_name),*args)
    
    def mdebug(self, *args) -> None:
        print("[{}]".format(self.module_name),*args)
        
    def saveTo(self, data: str, filename: t.Union[str, os.PathLike]) -> None:
        with open(filename, 'w+', encoding='utf-8') as file:
            file.write(data)
