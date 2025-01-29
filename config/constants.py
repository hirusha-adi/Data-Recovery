import os
import tempfile
import time
from getpass import getuser
from pathlib import Path

class Constant:

    # Modes and Stuff for Script
    # -----------------------------------
    QUIET_MODE: bool = False
    LOG_TO_FILE: bool = True

    # Save Formats
    # -----------------------------------
    browser_history_csv: bool = True
    browser_history_json: bool = True

    browser_bookmark_csv: bool = True
    browser_bookmark_json: bool = True

    # Paths and Stuff
    # -----------------------------------

    # Base Stuff
    datetime: str = time.strftime("%d%m%Y_%H%M%S")
    main_folder_name: Path = Path.cwd()
    base_output_folder: str = "output"

    username: str = getuser()
    temp_dir: Path = Path(tempfile.gettempdir())
    local_dir: Path = Path(os.getenv("LOCALAPPDATA", ""))
    roaming_dir: Path = Path(os.getenv("APPDATA", ""))
    userprofile_dir: Path = Path(os.getenv("USERPROFILE", ""))
    
    log_filename: str = f"{username}-{datetime}.log"

    # Final Output Paths
    final_output_folder: Path = main_folder_name / base_output_folder
    final_output_folder_user: Path = final_output_folder / username
    made_once: bool = False

    # File Content
    separator: str = "\n\n" + "=" * 20 + "\n\n"
    
    class Args:
        """
        Store states of command-line arguments for script behavior.
        """
        silent: bool = False
        verbose: bool = True
        log: bool = True
