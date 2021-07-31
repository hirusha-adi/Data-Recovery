import subprocess
import os
from datetime import datetime
import time
import json
import forall

def WIFI_PASSWORD_EXTRACTOR():

    output_filename = f'{forall.USER_NAME()}\\wifi_passwords.txt'

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

    print("\n")


    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                print ("{:<30}|  {:<}".format(i, results[0]))
                file.write("\n{:<30}|  {:<}".format(i, results[0]))
            except IndexError:
                print ("{:<30}|  {:<}".format(i, ""))
                file.write("\n{:<30}|  {:<}".format(i, ""))
        except subprocess.CalledProcessError:
            print ("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
            file.write("\n{:<30}|  {:<}".format(i, "ENCODING ERROR"))
        except Exception as e:
            print("Error: ", e)

    try:
        file.write(f"\n\n{datetime.now()} - Finished\n\nMade by ZeaCeR#5641")
        file.close()
        print("\n")
    except Exception as e:
        print("Error: ", e)

    
    jfile = open("config.json", "r", encoding="utf-8")
    jsonfile = json.loads(jfile.read())
    jfile.close()

    tts = jsonfile["wifi-pass-extractor"]["sleep-time-last"]
    if tts == 0:
        pass
    else:
        time.sleep(tts)

# WIFI_PASSWORD_EXTRACTOR()