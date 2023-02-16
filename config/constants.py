import os
import random
import string
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

    # Stuff about Computer
    username = getuser()
    temp_dir = tempfile.gettempdir()
    
    # Log file name
    log_filename = f'{username}-{datetime}.log'

    # File Content
    seperator = "\n\n" + "="*20 + "\n\n"
    
    # Arguments
    class Args:
        silent = True
        verbose = False
        log = False
        