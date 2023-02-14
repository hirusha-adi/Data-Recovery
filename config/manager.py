import os
import typing as t
from datetime import datetime

from config.constants import Constant


class ModuleManager:
    
    def __init__(self, module_name:str) -> None:
        
        # ########## Module Related ##########
        self.module_name = module_name

        # ########## File/Directory Names ##########
        self.output_folder = os.path.join(Constant.main_folder_name, Constant.base_output_folder)
        self.output_folder_user = os.path.join(Constant.main_folder_name, Constant.base_output_folder, Constant.username)
        self.log_filename = os.path.join(self.output_folder_user, Constant.log_filename)
        
        # ########## Main User Directory ##########
        if not os.path.exists(self.output_folder_user):
            os.makedirs(self.output_folder_user)
        else:
            i = 1
            while True:
                user_dir = os.path.join(self.output_folder, f'{Constant.username}-{i}')
                if not os.path.exists(user_dir):
                    os.makedirs(user_dir)
                    break
                i += 1
                
        # ########## Log File ##########
        if Constant.LOG_TO_FILE:
            if not os.path.isfile():
                with open(self.log_filename, 'w', encoding='utf-8') as _file:
                    _file.write(f'[{datetime.now()}] [ModuleManager] -> Log File Created')

    # ########## Print Functions - Colored ##########
    
    def mprint(self, *args) -> None:
        print("[{}]".format(self.module_name), *args)
    
    def merror(self, *args) -> None:
        print("[{}]".format(self.module_name),*args)
    
    def mdebug(self, *args) -> None:
        print("[{}]".format(self.module_name),*args)
        
    # ########## Log To File Stuff ##########

    def log(self, *args) -> None:
        if Constant.LOG_TO_FILE:
            with open(self.log_filename, 'w+', encoding='utf-8') as file:
                file.write(f"[{datetime.now()}] [{self.module_name}] -> {' '.join(args)}")
    
    # ########## Save Data to File ##########
    
    def saveTo(self, data: str, filename: t.Union[str, os.PathLike]) -> None:
        with open(filename, 'w+', encoding='utf-8') as file:
            file.write(data)

