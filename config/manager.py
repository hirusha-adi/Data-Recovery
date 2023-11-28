import os
import typing as t
from datetime import datetime

from config.constants import Constant
from config.colors import Colors


class ModuleManager:

    def __init__(self, module_name: str) -> None:

        # ########## Module Related ##########
        self.module_name = module_name

        # ########## File/Directory Names ##########
        self.output_folder = Constant.final_output_folder
        self.output_folder_user = Constant.final_output_folder_user

        # ########## Main User Directory ##########
        if not Constant.made_once:
            if not os.path.exists(self.output_folder_user):
                os.makedirs(self.output_folder_user)
                if not (Constant.Args.silent):
                    print("="*20, "\nFolder Doesnt exist:",
                          self.output_folder_user)
                Constant.made_once = True

        self.log_filename = os.path.join(
            Constant.final_output_folder_user, Constant.log_filename)

        # ########## Log File ##########
        if Constant.LOG_TO_FILE:
            if not os.path.isfile(self.log_filename):
                with open(self.log_filename, 'w', encoding='utf-8') as _file:
                    _file.write(
                        f'[{datetime.now()}] [ModuleManager] -> Log File Created')

    # ########## Print Functions - Colored ##########

    def banner(self, *args, **kwargs) -> None:
        if not (Constant.Args.silent):
            print(*args, **kwargs)

    def mprint(self, *args) -> None:
        if not (Constant.Args.silent):
            print("[{}]".format(self.module_name), *args)

        if Constant.Args.log:
            self.log(*args)

    def merror(self, *args) -> None:
        if not (Constant.Args.silent):
            print("{color}[{module_name}] [ERROR]".format(
                color=Colors.RED, module_name=self.module_name), *args, end=f"{Colors.RESET}\n")

        if Constant.Args.log:
            self.log('[ERROR]', *args)

    def mdebug(self, *args) -> None:
        c = not (Constant.Args.silent) and Constant.Args.verbose
        if c:
            print("{color}[{module_name}] [DEBUG]".format(
                color=Colors.GREY, module_name=self.module_name), *args, end=f"{Colors.RESET}\n")

        if Constant.Args.log:
            self.log('[DEBUG]', *args)

    # ########## Log To File Stuff ##########

    def log(self, *args) -> None:
        if Constant.LOG_TO_FILE:
            with open(self.log_filename, 'a', encoding='utf-8') as file:
                file.write(
                    f"\n[{datetime.now()}] [{self.module_name}] -> {' '.join(args)}")

    # ########## Save Data to File ##########

    def saveTo(self, data: str, filename: t.Union[str, os.PathLike]) -> None:
        with open(filename, 'w+', encoding='utf-8') as file:
            file.write(data)
