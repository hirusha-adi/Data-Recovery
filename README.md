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

( "yes" for true and "no" for false )

# How to compile ( from `.py` to `.exe` )

```
pyinstaller --noconfirm --onefile --console --icon "logo.ico" "runall.py"
```
