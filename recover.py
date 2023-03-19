import sys


from config import Constant
from config import Colors

from modules import ChromiumRecovery, WebHistoryRecovery, WebBookmarksRecovery  # browser
from modules import NetworkInfoRecovery, WifiPasswordRecovery  # network
from modules import SystemInfoRecovery  # system


class args:
    all = False
    browser_all = False
    browser_passwords = False
    browser_history = False
    browser_bookmakrs = False
    network_all = False
    network_wifi = False
    network_info = False
    system_all = False


def parser():

    __help_message = r"""
usage: recover.py [-h] [--silent] [--verbose] [--log] [--all] [--browser-all] [--browser-passwords] [--browser-history] [--browser-bookmakrs] [--network-all]
                  [--network-wifi] [--network-info] [--system-all]

Data Recovery | Built by @hirusha-adi

options:
  -h, --help            show this help message and exit
  --silent, -s          Silent Mode - No Console Output
  --verbose, -v         Verbose - Display everything that happens
  --log, -l             Log to file
  --all, -a             Get All Information
  --browser-all, -ba    Get Browser Passwords, Cookies, Cards and History and Bookmarks
  --browser-passwords, -bp
                        Get Browser Passwords, Cookies, Cards and History DB File
  --browser-history, -bh
                        Get Browser History
  --browser-bookmakrs, -bb
                        Get Browser Bookmarks
  --network-all, -na    Get All Network Information and Wifi Passwords
  --network-wifi, -nw   Get Wifi Passwords
  --network-info, -ni   Get All Network Information
  --system-all, -sa     Get All Network Information and Wifi Passwords
    """

    argsv = sys.argv[:]

    if ("--help" in argsv) or ("-h" in argsv):
        print(__help_message)
        exit()

    # Silent mode
    if ("--silent" in argsv) or ("-s" in argsv):
        Constant.Args.silent = False
        Constant.Args.verbose = False
        Constant.Args.log = False
    elif ("--verbose" in argsv) or ("-v" in argsv) or ("--log" in argsv) or ("-l" in argsv):
        # Verbose
        if ("--verbose" in argsv) or ("-v" in argsv):
            Constant.Args.verbose = True
        # Log to File
        if ("--log" in argsv) or ("-l" in argsv):
            Constant.Args.log = False
    else:
        # Default if no args
        Constant.Args.silent = False
        Constant.Args.verbose = True
        Constant.Args.log = True


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
        ChromiumRecovery().run()

    if Constant.Args.browser_history:
        WebHistoryRecovery().run()

    if Constant.Args.browser_bookmakrs:
        WebBookmarksRecovery().run()

    if Constant.Args.network_wifi:
        WifiPasswordRecovery().run()

    if Constant.Args.network_info:
        NetworkInfoRecovery().run()

    if Constant.Args.system_all:
        SystemInfoRecovery().run()

    cexit()


if __name__ == "__main__":
    main()
