import subprocess
from pathlib import Path

from config.manager import ModuleManager


class SystemInfoRecovery(ModuleManager):
    """
    Module for gathering system information and saving it to files.
    """
    def __init__(self) -> None:
        super().__init__(module_path="systeminfo/general")
        
        self.banner(r"""
         _______          ______                              
        |.-----.|        / _____)             _               
        ||x . x||       ( (____  _   _  ___ _| |_ _____ ____  
        ||_.-._||        \____ \| | | |/___|_   _) ___ |    \ 
        `--)-(--`        _____) ) |_| |___ | | |_| ____| | | |
       __[=== o]___     (______/ \__  (___/   \__)_____)_|_|_|
      |:::::::::::|\            (____/                        
      `-=========-`()                Information
                    """)

        self.systeminfo_filename: Path = self.module_output / "systeminfo.txt"
        self.computerinfo_filename: Path = self.module_output / "computerinfo.txt"
        self.motherboard_filename: Path = self.module_output / "motherboard.txt"
        self.cpu_filename: Path = self.module_output / "cpu.txt"
        self.sounds_filename: Path = self.module_output / "sounds.txt"

    def systeminfo(self) -> None:
        self.exec_n_save(["systeminfo"], self.systeminfo_filename, sub_module_name="systeminfo")
    
    def computerinfo(self) -> None:
        self.exec_n_save(["powershell", "Get-ComputerInfo"], self.computerinfo_filename, sub_module_name="computerinfo")
    
    def motherboard(self) -> None:
        self.exec_n_save(["powershell", "Get-WmiObject win32_baseboard"], self.motherboard_filename, sub_module_name="motherboard")
    
    def cpu(self) -> None:
        self.exec_n_save(["powershell", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property [a-z]*"], self.cpu_filename, sub_module_name="cpu")
    
    def sound(self) -> None:
        self.exec_n_save(["powershell", "Get-CimInstance win32_sounddevice | fl *"], self.sounds_filename, sub_module_name="sound")

    def run(self) -> None:
        __funcs__ = (
            "systeminfo", "computerinfo", 
            "motherboard", "cpu", "sound"
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
