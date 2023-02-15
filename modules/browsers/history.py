from browser_history import get_history
import getpass
import os
from datetime import datetime

def WEB_HISTORY_EXTRACTOR():

    printyn = forall.LOAD_JSON()["web-browser-history-extractor"]["print-y-n"]
    output_filename_csv = f'{forall.USER_NAME()}\\browser_history_all.csv'
    output_filename_json = f'{forall.USER_NAME()}\\browser_history_all.json'

    try:
        os.mkdir(forall.USER_NAME())
    except Exception as e:
        print("Error: ", e)

    outputs = get_history()
    his = outputs.histories

    for i in his:
        print(f'\n\n{i[0]} - {i[1]}')
    
    try:
        outputs.save(f'{output_filename_csv}')
    except Exception as e:
        print("Error: ", e)

    try:
        outputs.save(f'{output_filename_json}')
    except Exception as e:
        print("Error: ", e)
