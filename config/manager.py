import os, sys, subprocess
import typing as t
from datetime import datetime
from pathlib import Path
from loguru import logger

from config.constants import Constant
from config.colors import Colors

class ModuleManager:
    """
    A base class to be inherited by other modules, providing logging, 
    directory management, and standardized output functionalities.
    """

    def __init__(self, module_path: t.Union[str, Path], module_name: t.Optional[str] = None) -> None:

        # ########## Module Related ##########
        self.module_name: str = module_name or self.__class__.__name__

        # ########## File/Directory Names ##########
        self.output_folder: Path = Path(Constant.final_output_folder)
        self.output_folder_user: Path = Path(Constant.final_output_folder_user)
        self.module_output: Path = self.output_folder_user / module_path

        self.log_filename: Path = self.output_folder_user / Constant.log_filename

        # ########## Initialize Stuff ##########
        self._initialize_directories()
        self._initialize_log_file()

        self._initialize_logger()

    # ########## Initialize Stuff ##########

    def _initialize_logger(self) -> None:
        """Configure loguru to write logs to a new file every time the program runs."""
        log_file = self.log_filename
        
        if Constant.Args.log and not Constant.Args.silent:
            logger.remove()  # Remove any previous logger configurations
            
            logger.add(log_file, rotation="1 week", encoding="utf-8", level="DEBUG")
            logger.add(sys.stdout, level="DEBUG")

    def _initialize_directories(self) -> None:
        """Ensure required directories exist before proceeding."""
        # main output folder of user
        # make it only once - first run
        if not Constant.made_once:
            self.output_folder_user.mkdir(parents=True, exist_ok=True)
            if not Constant.Args.silent:
                print("=" * 20, "\nCreating folder:", self.output_folder_user)
            Constant.made_once = True
        
        # module output folder
        self.module_output.mkdir(parents=True, exist_ok=True)
        print("=" * 20, "\nCreating folder:", self.module_output)
    
    def _initialize_log_file(self) -> None:
        """Create log file if logging is enabled and file does not exist."""
        if Constant.LOG_TO_FILE and not self.log_filename.exists():
            self.log_filename.write_text(f'[{datetime.now()}] [ModuleManager] -> Log File Created\n', encoding='utf-8')

    # ########## Logging ##########

    def banner(self, *args, **kwargs) -> None:
        if not (Constant.Args.silent):
            print(*args, **kwargs)

    def mprint(self, *args: t.Any) -> None:
        if Constant.Args.log and not Constant.Args.silent:
            logger.info(f"[{self.module_name}] " + " ".join(map(str, args)))
    
    def merror(self, *args: t.Any) -> None:
        if Constant.Args.log and not Constant.Args.silent:
            logger.error(f"[{self.module_name}] [ERROR] " + " ".join(map(str, args)))
    
    def mdebug(self, *args: t.Any) -> None:
        if Constant.Args.verbose and not Constant.Args.silent:
            logger.debug(f"[{self.module_name}] [DEBUG] " + " ".join(map(str, args)))

    # ########## Save Data to File ##########

    def save_to(self, data: str, filename: t.Union[str, Path]) -> None:
        """Save data to a specified file, ensuring the directory exists."""
        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(data, encoding='utf-8')

    # ########## Run and Save Output ##########

    def exec_n_save(self, command: list[str], output_file: Path, sub_module_name: t.Optional[str] = None) -> None:
        
        logger_beginning = f"[{self.module_name}] "
        if sub_module_name:
            logger_beginning += f"({sub_module_name}) "
        
        self.mprint(f"{logger_beginning} Running command: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, errors="backslashreplace", check=True)
            cleaned_output = result.stdout.replace("\r\n", "\n").strip()
            output_file.write_text(cleaned_output, encoding="utf-8")
            self.mprint(f"{logger_beginning} Output saved to {output_file}")

        except subprocess.CalledProcessError as e:
            self.merror(f"{logger_beginning} Command failed: {e}")

        except Exception as e:
            self.merror(f"{logger_beginning} Unexpected error: {e}", exc_info=True)
