import os
import tempfile
import time
from getpass import getuser


class Constant:

    # Modes and Stuff for Script
    # -----------------------------------

    QUIET_MODE = False
    LOG_TO_FILE = True

    # Save Formats
    # -----------------------------------
    browser_history_csv = True
    browser_history_json = True

    browser_bookmark_csv = True
    browser_bookmark_json = True

    # Paths and Stuff
    # -----------------------------------

    # Base Stuff
    datetime = time.strftime("%d%m%Y_%H%M%S")
    main_folder_name = os.getcwd()
    base_output_folder = 'output'

    username = getuser()
    temp_dir = tempfile.gettempdir()
    local_dir = os.getenv('LOCALAPPDATA')
    roaming_dir = os.getenv('APPDATA')
    
    log_filename = f'{username}-{datetime}.log'

    # Final Base Stuff
    final_output_folder = os.path.join(main_folder_name, base_output_folder)
    final_output_folder_user = os.path.join(
        main_folder_name, base_output_folder, username)
    made_once = False

    # File Content
    seperator = "\n\n" + "="*20 + "\n\n"
    
    # Arguments
    # -----------------------------------
    class Args:

        # Display Modes
        silent = False
        verbose = True
        log = True
