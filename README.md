# Data Recovery

This application is designed to help users recover lost or forgotten data such as Wi-Fi passwords, browser data, browser passwords, and other sensitive information from their computers.

With this application, users can easily recover lost or forgotten Wi-Fi passwords and other login credentials, as well as browsing history, bookmarks, and other web data. This makes it easy to recover data quickly.

The data recovery process is secure, as the application does not store or share any sensitive data. Additionally, the application is highly efficient, with fast scanning and recovery times, enabling users to recover their lost data quickly and easily.

# How to Setup?

1. Install Python
2. Run this command to use a Virtual Enviroment (This will help in a reduced compiled file size)

   ```
   python -m pip install virtualenv
   ```

3. Create a virtual enviroment

   ```
   virtualenv env
   ```

4. Activate the virtual enviroment

   ```
   env\Scripts\activate.bat
   ```

5. Install requirements

   ```
   pip install -r requirements.txt
   ```

6. Install PyInstaller to build the executable

   ```
   pip install pyinstaller
   ```

7. Run these commands to compile

   - Normal Mode

     ```
     pyinstaller recover.py --noconfirm --onefile --name "Data Recovery" --console
     ```

   - Hidden Mode

     ```
     pyinstaller recover.py --noconfirm --onefile --name "Data Recovery" --windowed
     ```

8. Deactive the virtual enviroment

   ```
   deactivate
   ```

Your compiled `Data Recovery.exe` is available at `./dist`

# Options

```
$ python .\recover.py --help

usage: [-h] [--silent] [--verbose] [--log] [--all] [--browser-all] [--browser-passwords] [--browser-history] [--browser-bookmakrs] [--network-all] [--network-wifi]
                  [--network-info] [--system-all]

Data Recovery | Built by @hirusha-adi

options:
  -h, --help            show this help message and exit
  --silent, -s          Silent Mode - No Console Output
  --verbose, -v         Verbose - Display everything that happens
  --log, -l             Log to file
  --all, -a             Get All Information
  --browser-all, -ba    Get Browser Passwords, Cookies, Cards and History and Bookmarks
  --browser-passwords, -bp
                        Get Browser Passwords, Cookies, Cards and History DB File
  --browser-history, -bh
                        Get Browser History
  --browser-bookmakrs, -bb
                        Get Browser Bookmarks
  --network-all, -na    Get All Network Information and Wifi Passwords
  --network-wifi, -nw   Get Wifi Passwords
  --network-info, -ni   Get All Network Information
  --system-all, -sa     Get All Network Information and Wifi Passwords
```

# Use Cases

- ## Data Recovery

  - You can easily recover data that has been lost using this tool

  - This is what this tool is made for

  - I do not encourage this to be used in occasion except for Data Recovery Purposes

- ## Data Stealer

  https://user-images.githubusercontent.com/36286877/127731137-c9c871cc-6e6d-4f95-9540-d7fd4332d683.mp4

  - I do not encourage anyone to use this tool for this malicious purpose and I am not responsible for anything done with this
  - This can be compiled with PyInstaller using the `--windowed` argument to not show any window while this is running

  - This can autorun on computers upto windows 10 if configured properly using tools like [SamLogic UBS AutoRun Creator](https://www.samlogic.net/usb-autorun-creator/usb-autorun-creator.htm)

    - It can be downloaded here: [link 1](https://www.samlogic.net/usb-autorun-creator/usb-autorun-creator.htm) / [link 2](https://download.cnet.com/SamLogic-USB-AutoRun-Creator/3000-2094_4-75724123.html) / [link 3](https://www.softpedia.com/get/System/System-Miscellaneous/USB-AutoRun-Creator.shtml)

    - Select the file .exe file inside the `dist` folder ( after compiling with pyinstaller ), select the pendrive and Click on the USB device you have plugged in, Enter any name as the Label and finally click `Create`. Wait some time for the software to generate and copy the necessary files.

![image](https://user-images.githubusercontent.com/36286877/127734445-f196d1a0-3d30-4788-a14e-9a38bd061272.png)

# Other Versions

- ## C++: [click here](https://github.com/hirusha-adi/Data-Recovery/tree/c++)

  - Very Small Executable
  - Comparatively faster than both Python Versions
