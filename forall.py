import os
import json
import getpass
from datetime import datetime

def LOAD_JSON():
    jfile = open("config.json", "r", encoding="utf-8")
    jsonfile = json.loads(jfile.read())
    jfile.close()
    return jsonfile

# def FILE_NAME(fileformat='txt'):
#     filename = getpass.getuser()
#     x = f'{filename}.{fileformat}'
#     return x

def USER_NAME():
    return getpass.getuser()

def LOG():
    return LOAD_JSON()["log-status"]

def LOGfile():
    try:
        os.mkrdir(f'{USER_NAME()}')
    except Exception as e:
        print("Error: ", e)
    return f'{USER_NAME()}\\{LOAD_JSON()["log-file-name"]}'

def checklog():
    try:
        flc = open(LOGfile(), "r")
        flc.close()
    except:
        try:
            if os.path.isfile(LOGfile()) == True:
                pass
            else:
                try:
                    filem = open(LOGfile(), "w", encoding="utf-8")
                    filem.write(f"{datetime.now()} - Log File Created")
                    filem.close()
                except Exception as e:
                    print("Error: ", e)
        except Exception as e:
            print("Error: ", e)

def runyn():
    return LOAD_JSON()["runningyn"]
    








