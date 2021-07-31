import os
import subprocess
from datetime import datetime
import forall

def SYSTEM_INFORMATION():

    output_filename = f'{forall.USER_NAME()}\\systeminfo.txt'

    try:
        os.mkdir(forall.USER_NAME())
    except Exception as e:
        print("Error: ", e)
    
    try:
        if os.path.isfile(output_filename) == True:
            pass
        else:
            try:
                filem = open(output_filename, "w", encoding="utf-8")
                filem.write(f"{datetime.now()} - File Created")
                filem.close()
            except Exception as e:
                print("Error: ", e)
            try:
                with open(output_filename, "w", encoding="utf-8") as fuck:
                    fuck.write(f"{datetime.now()} - File Created")
            except Exception as e:
                print("Error: ", e)

            file = open(output_filename, "r+", encoding="utf-8")
            file.write(f"{datetime.now()} - Starting program\n")

    except Exception as e:
        print("Error: ", e)

    data = subprocess.check_output(['systeminfo']).decode('utf-8', errors="backslashreplace")
    with open(output_filename, "w") as file:
        file.write(data)
        file.write("\n\nMade by ZeaCeR#5641")


# SYSTEM_INFORMATION()