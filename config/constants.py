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
    
    profile = {
        'HOMEDRIVE': u'{drive}:'.format(drive=drive),
        'HOMEPATH': u'{drive}:\\Users\\{user}'.format(drive=drive, user=username),
        'APPDATA': u'{drive}:\\Users\\{user}\\AppData\\Roaming\\'.format(drive=drive, user=username),
        'USERPROFILE': u'{drive}:\\Users\\{user}\\'.format(drive=drive, user=username),
        'COMPOSER_HOME': u'{drive}:\\Users\\{user}\\AppData\\Roaming\\Composer\\'.format(drive=drive, user=username),
        'LOCALAPPDATA': u'{drive}:\\Users\\{user}\\AppData\\Local'.format(drive=drive, user=username),
        'ALLUSERSPROFILE': u'{drive}:\\ProgramData'.format(drive=drive, user=username),
    }
    