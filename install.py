import os
import platform
import time

if platform.system() == 'Windows':
    clear = "cls"
    pip = "pip"
    py3 = "python"
else:
    clear = "clear"
    pip = "pip3"
    py3 = "python3"

try:
    try:
        os.system(f'{pip} install win32crypt')
    except:
        pass
    os.system(f'{pip} install pypiwin32')
    os.system(f'{pip} install pycryptodome')
    os.system(f'{pip} install browser-history')
    try:
        os.system(f'{pip} install browser-history')
    except:
        pass
except:
    pass

print("\n\n\nRan the commands needed to Run it!\n")
time.slep(10)



        