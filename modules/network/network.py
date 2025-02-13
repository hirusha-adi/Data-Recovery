import os
import subprocess
from pathlib import Path

from config import ModuleManager


class NetworkInfoRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_path="network/general")
        
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
        self.exec_n_save(["ipconfig", "/all"], self.ipconfig_filename, sub_module_name="ipinfo")
    
    def ipconfiguration(self) -> None:
        self.exec_n_save(["powershell", "get-wmiobject Win32_NetworkAdapterConfiguration"], self.ipconfiguration_filename, sub_module_name="ipconfiguration")

    def physical_adapters(self) -> None:
        self.exec_n_save(["powershell", "Get-NetAdapter -physical| where status -eq 'up'"], self.physical_adapters_filename, sub_module_name="physical_adapters")

    def getnet_ipconfig(self) -> None:
        self.exec_n_save(["powershell", "Get-NetIPConfiguration -All"], self.getnet_ipconfig_filename, sub_module_name="getnet_ipconfig")

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
