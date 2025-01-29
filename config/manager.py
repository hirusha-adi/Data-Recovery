import os
import typing as t
from datetime import datetime
from pathlib import Path

from config.constants import Constant
from config.colors import Colors


class ModuleManager:
    """
    A base class to be inherited by other modules, providing logging, 
    directory management, and standardized output functionalities.
    """

    def __init__(self, module_name: str) -> None:

        # ########## Module Related ##########
        self.module_name: str = module_name

        # ########## File/Directory Names ##########
        self.output_folder: Path = Path(Constant.final_output_folder)
        self.output_folder_user: Path = Path(Constant.final_output_folder_user)

        self.log_filename: Path = self.output_folder_user / Constant.log_filename

        # ########## Initialize Stuff ##########
        self._initialize_directories()
        self._initialize_log_file()

    # ########## Initialize Stuff ##########

    def _initialize_directories(self) -> None:
        """Ensure required directories exist before proceeding."""
        if not Constant.made_once:
            self.output_folder_user.mkdir(parents=True, exist_ok=True)
            if not Constant.Args.silent:
                print("=" * 20, "\nCreating folder:", self.output_folder_user)
            Constant.made_once = True
    
    def _initialize_log_file(self) -> None:
        """Create log file if logging is enabled and file does not exist."""
        if Constant.LOG_TO_FILE and not self.log_filename.exists():
            self.log_filename.write_text(f'[{datetime.now()}] [ModuleManager] -> Log File Created\n', encoding='utf-8')

    # ########## Print Functions - Colored ##########

    def banner(self, *args, **kwargs) -> None:
        if not (Constant.Args.silent):
            print(*args, **kwargs)

    def mprint(self, *args: t.Any) -> None:
        """Module-specific print function with optional logging."""
        if not Constant.Args.silent:
            print(f"[{self.module_name}]", *args)
        if Constant.Args.log:
            self.log(*args)
    
    def merror(self, *args: t.Any) -> None:
        """Print error messages in red with logging support."""
        if not Constant.Args.silent:
            print(f"{Colors.RED}[{self.module_name}] [ERROR]", *args, f"{Colors.RESET}")
        if Constant.Args.log:
            self.log("[ERROR]", *args)
    
    def mdebug(self, *args: t.Any) -> None:
        """Print debug messages in grey if verbose mode is enabled."""
        if Constant.Args.verbose and not Constant.Args.silent:
            print(f"{Colors.GREY}[{self.module_name}] [DEBUG]", *args, f"{Colors.RESET}")
        if Constant.Args.log:
            self.log("[DEBUG]", *args)

    # ########## Log To File Stuff ##########

    def log(self, *args: t.Any) -> None:
        """Append log messages to the log file if logging is enabled."""
        if Constant.LOG_TO_FILE:
            with self.log_filename.open('a', encoding='utf-8') as file:
                file.write(f"[{datetime.now()}] [{self.module_name}] -> {' '.join(map(str, args))}\n")

    # ########## Save Data to File ##########

    def save_to(self, data: str, filename: t.Union[str, Path]) -> None:
        """Save data to a specified file, ensuring the directory exists."""
        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(data, encoding='utf-8')
