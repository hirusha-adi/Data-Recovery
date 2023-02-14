# -*- coding: utf-8 -*- 

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
    
    
    # Paths and Stuff
    # -----------------------------------
    
    # Stuff needed to grabbing data
    main_folder_name = os.getcwd()

    # Stuff about Computer
    username = getuser()
    drive = u'C'
    temp_dir = tempfile.gettempdir()
