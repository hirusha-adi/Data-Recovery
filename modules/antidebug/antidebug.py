"""
Source code is taken and modified from:
    https://github.com/xtekky/Python-Anti-Debug/blob/main/anti-debug.py

Anti-Debugger + SSL-Pinning, to defeat fiddlers (distinguish debug-proxied connection and secure ur programs)
"""

import difflib
import os
import platform
import socket
import ssl
import subprocess
import threading
import winreg

import getmac
import OpenSSL
import psutil
import requests
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut

from modules.antidebug.data import *
from config import Constant
from config import ModuleManager

class SSLPinner:
    def __init__(self, host):
        self.host = host

    def similar(self, a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()

    def get_cert(self):
        try:
            context = ssl.create_default_context()
            conn = socket.create_connection((self.host, 443))
            sock = context.wrap_socket(conn, server_hostname=self.host)
            sock.settimeout(10)
            try:
                der_cert = sock.getpeercert(True)
            finally:
                sock.close()
            return ssl.DER_cert_to_PEM_cert(der_cert)
        except:
            return False

    def pin(self):
        certificate = self.get_cert()
        if not certificate:
            return False

        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

        result = {
            "subject": dict(x509.get_subject().get_components()),
            "issuer": dict(x509.get_issuer().get_components()),
            "serialNumber": x509.get_serial_number(),
            "version": x509.get_version(),
        }

        extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
        extension_data = {e.get_short_name(): str(e) for e in extensions}
        result.update(extension_data)

        _str = r"{'subject': {b'CN': b'*.tiktok.com'}, 'issuer': {b'C': b'US', b'O': b'DigiCert Inc', b'CN': b'RapidSSL TLS DV RSA Mixed SHA256 2020 CA-1'}, 'serialNumber': 10563365078873817837960662065118294014, 'version': 2, b'authorityKeyIdentifier': 'keyid:A4:8D:E5:BE:7C:79:E4:70:23:6D:2E:29:34:AD:23:58:DC:F5:31:7F\n', b'subjectKeyIdentifier': '82:95:09:E5:DB:5F:56:24:04:A2:D5:CA:C6:98:02:18:7B:11:4A:D3', b'subjectAltName': 'DNS:*.tiktok.com, DNS:tiktok.com', b'keyUsage': 'Digital Signature, Key Encipherment', b'extendedKeyUsage': 'TLS Web Server Authentication, TLS Web Client Authentication', b'crlDistributionPoints': '\nFull Name:\n  URI:http://crl3.digicert.com/RapidSSLTLSDVRSAMixedSHA2562020CA-1.crl\n\nFull Name:\n  URI:http://crl4.digicert.com/RapidSSLTLSDVRSAMixedSHA2562020CA-1.crl\n', b'certificatePolicies': 'Policy: 2.23.140.1.2.1\n  CPS: http://www.digicert.com/CPS\n', b'authorityInfoAccess': 'OCSP - URI:http://ocsp.digicert.com\nCA Issuers - URI:http://cacerts.digicert.com/RapidSSLTLSDVRSAMixedSHA2562020CA-1.crt\n', b'basicConstraints': 'CA:FALSE', b'ct_precert_scts': 'Signed Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 29:79:BE:F0:9E:39:39:21:F0:56:73:9F:63:A5:77:E5:\n                BE:57:7D:9C:60:0A:F8:F9:4D:5D:26:5C:25:5D:C7:84\n    Timestamp : Aug 20 06:34:51.301 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:44:02:20:3E:E4:D6:59:EC:22:65:35:0B:56:33:D3:\n                55:C6:E6:3D:48:C5:4A:D0:BA:8D:FD:6E:0F:9B:90:0A:\n                8A:73:FC:DB:02:20:6E:4B:5E:EA:EF:EE:AD:A9:FA:F1:\n                77:2E:28:87:58:D1:AF:C3:9B:96:6D:CB:19:80:03:CF:\n                A7:7D:6C:49:55:88\nSigned Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 51:A3:B0:F5:FD:01:79:9C:56:6D:B8:37:78:8F:0C:A4:\n                7A:CC:1B:27:CB:F7:9E:88:42:9A:0D:FE:D4:8B:05:E5\n    Timestamp : Aug 20 06:34:51.407 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:46:02:21:00:FA:94:CD:71:C1:9D:58:0F:26:84:7C:\n                BF:E9:28:BB:AF:89:8C:DB:19:C3:4C:CA:E5:A0:62:D2:\n                FB:3E:24:1E:9B:02:21:00:AC:D4:22:35:BC:09:5C:9E:\n                89:10:A9:4B:AA:B1:2D:32:D3:E1:55:67:5E:F9:CF:F0:\n                25:D0:1C:5B:72:06:AC:C2\nSigned Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 41:C8:CA:B1:DF:22:46:4A:10:C6:A1:3A:09:42:87:5E:\n                4E:31:8B:1B:03:EB:EB:4B:C7:68:F0:90:62:96:06:F6\n    Timestamp : Aug 20 06:34:51.325 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:46:02:21:00:91:61:96:CC:4F:6E:0D:C1:2A:EF:25:\n                06:89:BB:2B:DB:71:31:45:F8:A9:20:04:B7:4C:CB:28:\n                1E:A8:47:DA:48:02:21:00:82:77:71:59:94:7C:B1:F8:\n                B7:79:14:05:0B:A1:C5:AD:05:08:F1:C8:C1:B8:6A:7A:\n                CA:3B:6A:A1:54:52:C9:B7'}"

        if self.similar(str(result), _str) > 0.8:
            return True
        else:
            return False


class Antidebug(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="AntiDebug")
        
        self.banner("""
     _______         _______            _    ______        _                 
    |.-----.|       (_______)       _  (_)  (______)      | |                
    ||x . x||        _______ ____ _| |_ _    _     _ _____| |__  _   _  ____ 
    ||_.-._||       |  ___  |  _ (_   _) |  | |   | | ___ |  _ \| | | |/ _  |
    `--)-(--`       | |   | | | | || |_| |  | |__/ /| ____| |_) ) |_| ( (_| |
   __[=== o]___     |_|   |_|_| |_| \__)_|  |_____/ |_____)____/|____/ \___ |
  |:::::::::::|\                                                      (_____|
  `-=========-`()   
                  """)
        
        self.timeout = 1.5
        try:
            self.isOnline = self.isConnected()
        except FunctionTimedOut:
            self.merror("User is NOT connected to the internet")
            self.isOnline = False
            
    @func_set_timeout(1.6)
    def isConnected(self) -> bool:
        try:
            response = requests.get('https://www.google.com', timeout=self.timeout)
            if response.status_code == 200:
                self.mdebug("User is connected to the internet")
                return True
            else:
                self.merror("User is NOT connected to the internet")
                return False
        except:
            self.merror("User is NOT connected to the internet")
            return False

    def _exit(self):
        # https://emojicombos.com/fuck-you-ascii-art
        self.banner("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣤⡶⠶⠟⠛⠛⠛⠋⠙⠛⠛⠿⢶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣴⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣽⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⠃⠀⠀⢰⡶⠾⠿⠿⠛⠛⠻⣿⠋⠀⠀⢸⡟⠉⠉⣭⣍⢹⡿⣷⡀⠀⠀⠀⠀⠀⠀⠀
⠀⣾⠃⠀⠀⠀⣿⡀⠀⠀⠰⠿⠆⣠⡿⠀⠀⠀⠈⢷⣤⣀⣼⡿⠟⠀⠹⣷⠀⠀⠀⠀⠀⠀⠀
⢸⡟⠀⠀⠀⠀⠘⠿⣶⣤⣤⣶⠾⠟⠁⠀⠀⠀⠀⠀⠈⠉⣁⣀⣀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀
⢸⡇⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⡶⠶⠶⠶⠶⠖⠛⠛⠛⠛⣿⠋⠉⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀
⣺⡇⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⣼⡇⠀⠀⠀⣤⡄⠀
⠸⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⠀⢠⡿⠁⠀⣠⣾⠏⠀⠀⠀⢀⣿⣇⠀
⠀⠹⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣦⠟⠁⣠⣾⠟⠁⠀⠀⠀⠀⣿⠉⣽⠂
⠀⠀⠈⠻⢷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠋⣹⣿⣴⡿⠋⠀⠀⢀⣠⣤⣶⣿⡽⠞⠁⠀
⠀⠀⠀⠀⠀⣸⡿⠻⠿⢶⣶⣶⣶⣶⣶⠶⣛⣷⡾⠛⠉⣿⣁⣠⠴⢞⣫⡵⠟⠋⠁⠀⠀⠀⠀
⠀⠀⠀⠀⣰⡟⠀⠀⢀⣤⡴⠟⣋⣥⡶⠚⠋⠁⠀⠀⠀⣿⣋⣤⠶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⡿⠀⠀⠐⣋⣤⣶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣿⠃⠀⠀⠘⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    """)
        self.merror("Debug Mode / Sandbox Detected! Quitting Application.")
        return True

    @func_set_timeout(1.5)
    def user_check(self):
        try:
            USER = os.getlogin()
            if USER in USERS:
                self.merror(f"Username: {USER} is blacklisted")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def hwid_check(self):
        try:
            HWID = (
                subprocess.check_output(
                    r"wmic csproduct get uuid", creationflags=0x08000000
                )
                .decode()
                .split("\n")[1]
                .strip()
            )

            if HWID in HWIDS:
                self.merror(f"HWID: {HWID} is blacklisted")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def gpu_check(self):
        try:
            GPU = (
                subprocess.check_output(
                    r"wmic path win32_VideoController get name",
                    creationflags=0x08000000,
                )
                .decode()
                .strip("Name\n")
                .strip()
            )
            for gpu in GPUS:
                if gpu in GPU.split("\n"):
                    self.merror(f"GPU: {gpu} is blacklisted")
                    self._exit()

        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def name_check(self):
        try:
            NAME = os.getenv("COMPUTERNAME")
            if NAME in NAMES:
                self.merror(f"Computer Name: {NAME} is blacklisted")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def path_check(self):
        try:
            for path in [r"D:\Tools", r"D:\OS2", r"D:\NT3X"]:
                if os.path.exists(path):
                    self.merror(f"PATH: {path} is blacklisted")
                    self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def platform_check(self):
        try:
            PLATFORM = str(platform.version())
            if PLATFORM in PLATFORMS:
                self.merror(f"Platform: {PLATFORM} is blacklisted")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def ip_check(self):
        try:
            if self.isOnline:
                IP = requests.get("https://api.myip.com").json()["ip"]
                if IP in IPS:
                    self.merror(f"IP Address: {IP} is blacklisted")
                    self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def mac_check(self):
        try:
            MAC = str(getmac.get_mac_address())
            if MAC in MACS:
                self.merror(f"MAC Address: {MAC} is blacklisted")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def registry_check(self):
        try:
            reg1 = os.system(
                "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul"
            )
            reg2 = os.system(
                "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul"
            )
            if reg1 != 1 and reg2 != 1:
                self._exit()

            handle = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum"
            )
            try:
                reg_val = winreg.QueryValueEx(handle, "0")[0]
                if ("VMware" or "VBOX") in reg_val:
                    self.merror(f"Virtual Machine Detected")
                    self._exit()
            finally:
                winreg.CloseKey(handle)
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")
            
    @func_set_timeout(1.5)
    def dll_check(self):
        try:
            vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
            virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")

            if os.path.exists(vmware_dll):
                self.merror(f"Virtual Machine Detected: VMWare: from {vmware_dll}")
                self._exit()
            if os.path.exists(virtualbox_dll):
                self.merror(f"Virtual Machine Detected: VirtualBox: from {virtualbox_dll}")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def specs_check(self):
        try:
            RAM = str(psutil.virtual_memory()[0] / 1024**3).split(".")[0]
            DISK = str(psutil.disk_usage("/")[0] / 1024**3).split(".")[0]

            if int(RAM) <= 2:
                self.merror(f"Invalid RAM Amount")
                self._exit()
            if int(DISK) <= 50:
                self.merror(f"Invalid Disk Space RAM Amount")
                self._exit()
            if int(psutil.cpu_count()) <= 1:
                self.merror(f"Invalid CPU Count")
                self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def proc_check(self):
        try:
            processes = ["VMwareService.exe", "VMwareTray.exe"]
            for proc in psutil.process_iter():
                for program in processes:
                    if proc.name() == program:
                        self.merror(f"Virtual Machine Detected: VMWare: from {proc.name()}")
                        self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    @func_set_timeout(1.5)
    def ssl_check(self):
        try:
            if self.isOnline:
                if SSLPinner("tiktok.com").pin():
                    self.merror(f"Bad result from SSL Pinner")
                    self._exit()
        except Exception as e:
            self.mdebug(f"[ERROR]: {e}")

    # No timout for this function as it keeps always running
    # @func_set_timeout(1.5)
    def process_check(self):
        self.mdebug(f"Running `process_check()` in a new Thread - Will kill any suspicous process if any")
        while True:
            for proc in psutil.process_iter():
                if any(procstr in proc.name().lower() for procstr in PROCESSES):
                    try:
                        self.mdebug(f"Killed process: {proc.name()}")
                        proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        self.merror(f"[ERROR]: Unable to kill {proc.name()} -> Access Denied | This could be a debugging application")
                    except Exception as e:
                        self.merror(f"[ERROR]: {e} | This could be a debugging application")

    def isDebugMode(self):
        try:
            __funcs__ = (
                'path_check', 'gpu_check', 'hwid_check', 'user_check', 'name_check', 
                'platform_check', 'ip_check', 'mac_check', 'proc_check', 'registry_check', 
                'specs_check', 'ssl_check'
            )
            
            for func_name  in __funcs__:
                try:
                    self.mdebug(f"Running function/check: `{func_name}()`")
                    func = getattr(self, func_name)
                    func()
                    self.mdebug(f"Ran function/check: `{func_name}()` Successfully")
                except TimeoutError:
                    pass
                
            threading.Thread(target=self.process_check).start()
            return False
        except Exception as e:
            self.merror(f"{e}")
