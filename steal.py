import argparse

from modules import *
from config import Constant


HELP = """
update.exe 
"""

def parser():
    parser = argparse.ArgumentParser(description="Data Stealer | Another Data Recovery Tool | Built by @hirusha-adi")
    parser.add_argument("--silent", "-s" , action="store_true", help="Silent Mode - No Console Output", default=True)
    parser.add_argument("--verbose", "-v" , action="store_true", help="Verbose - Display everything that happens", default=False)
    parser.add_argument("--log", "-l" , action="store_true", help="Log to file", default=False)
    
    args = parser.parse_args()
    
    Constant.Args.silent = args.silent
    Constant.Args.verbose = args.verbose
    Constant.Args.log = args.log
    
    if Constant.Args.silent:
        Constant.Args.verbose = False
        Constant.Args.silent = False
        Constant.Args.log = False
    

def main():
    parser()
    
    if Antidebug().isDebugMode():
        exit()
    else:
        pass

if __name__ == "__main__":
    main()