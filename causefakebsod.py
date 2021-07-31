import os
import forall

def CAUSE_FAKE_BSOD():

    yorn = forall.LOAD_JSON()["bsod"]["yn"]
    shutdownyn = forall.LOAD_JSON()["bsod"]["shutdown"]

    if yorn == "yes":

        if shutdownyn == "no":
            os.system("bluescreen.exe")
        else:
            os.system("bluescreenshutdown.exe")







