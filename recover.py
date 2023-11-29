import sys


from config import Constant
from config import Colors

from modules import ChromiumRecovery, WebHistoryRecovery, WebBookmarksRecovery  # browser
from modules import NetworkInfoRecovery, WifiPasswordRecovery  # network
from modules import SystemInfoRecovery  # system
from modules import DiscordRecovery # applications

class args:
    browser_passwords = False
    browser_history = False
    browser_bookmakrs = False
    network_wifi = False
    network_info = False
    system_all = False
    applications_discord = False


def parser():

    __help_message = r"""
usage: [-h] [--silent] [--verbose] [--log] [--all] [--browser-all] [--browser-passwords] [--browser-history] [--browser-bookmakrs] [--network-all] [--network-wifi] [--network-info] [--system-all]

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
  --apps-discord, -ad   Get Discord Tokens of Logged in Accounts
    """

    argsv = sys.argv[:]

    if any(arg in argsv for arg in ["--help", "-h"]):
        print(__help_message)
        sys.exit()

    # Silent mode
    if any(arg in argsv for arg in ["--silent", "-s"]):
        Constant.Args.silent = True
        Constant.Args.verbose = False
        Constant.Args.log = False
    elif any(arg in argsv for arg in ["--verbose", "-v", "--log", "-l"]):
        # Verbose
        if any(arg in argsv for arg in ["--verbose", "-v"]):
            Constant.Args.verbose = True
        # Log to File
        if any(arg in argsv for arg in ["--log", "-l"]):
            Constant.Args.log = True
    else:
        # Default if no args
        Constant.Args.silent = False
        Constant.Args.verbose = True
        Constant.Args.log = True
    if any(arg in argsv for arg in ["--log", "-l"]):
        Constant.Args.log = True

    # browser recovery
    if any(arg in argsv for arg in ["--browser-all", "-ba"]):
        args.browser_passwords = True
        args.browser_history = True
        args.browser_bookmakrs = True
    elif any(arg in argsv for arg in ["--browser-passwords", "-bp", "--browser-history", "-bh", "--browser-bookmakrs", "-bb"]):
        if any(arg in argsv for arg in ["--browser-passwords", "-bp"]):
            args.browser_passwords = True
        else:
            args.browser_passwords = False
        if any(arg in argsv for arg in ["--browser-history", "-bh"]):
            args.browser_history = True
        else:
            args.browser_bookmakrs = False
        if any(arg in argsv for arg in ["--browser-bookmakrs", "-bb"]):
            args.browser_bookmakrs = True
        else:
            args.browser_bookmakrs = False
    else:
        args.browser_passwords = False
        args.browser_bookmakrs = False
        args.browser_bookmakrs = False

    # network info
    if any(arg in argsv for arg in ["--network-all", "-na"]):
        args.network_wifi = True
        args.network_info = True
    elif any(arg in argsv for arg in ["--network-wifi", "-nw", "--network-info", "-ni"]):
        if any(arg in argsv for arg in ["--network-wifi", "-nw"]):
            args.network_wifi = True
        else:
            args.network_wifi = False
        if any(arg in argsv for arg in ["--network-info", "-ni"]):
            args.network_info = True
        else:
            args.network_info = False
    else:
        args.network_wifi = False
        args.network_info = False

    if any(arg in argsv for arg in ["--system-all", "-sa"]):
        args.system_all = True
    else:
        args.system_all = False
    
    # applications
    if any(arg in argsv for arg in ["--apps-discord", "-ad"]):
        args.applications_discord = True
    else:
        args.applications_discord = False
        
    if any(arg in argsv for arg in ["--all", "-a"]):
        args.browser_bookmakrs = True
        args.browser_history = True
        args.browser_passwords = True
        args.network_info = True
        args.network_wifi = True
        args.system_all = True

    if not (args.browser_passwords or args.browser_history or args.browser_bookmakrs or args.network_info or args.network_wifi or args.system_all or args.applications_discord):
        print(__help_message)
        sys.exit()


def cexit():
    if not (Constant.Args.silent):
        print(f"""
{Colors.GREEN}   __,_,
{Colors.GREEN}  [_|_/                {Colors.CYAN}   Made by {Colors.MAGENTA}{Colors.UNDERLINE}@hirusha-ad{Colors.RESET}
{Colors.GREEN}   //                  {Colors.CYAN} ------------------------
{Colors.GREEN} _//    __             {Colors.CYAN} 
{Colors.GREEN}(_|)   |@@|            {Colors.CYAN} Check out my other
{Colors.GREEN} \\ \\__ \\--/ __         {Colors.CYAN} projects at Github
{Colors.GREEN}  \\o__|----|  |   __   {Colors.CYAN} 
{Colors.GREEN}      \\ () /\\ )_ / _\\  {Colors.CYAN} Email ->
{Colors.GREEN}      /\\__/\\ \\__O (__  {Colors.CYAN}     {Colors.UNDERLINE}{Colors.MAGENTA}hirushaadi@gmail.com{Colors.RESET}
{Colors.GREEN}     (--/\\--)    \\__/  {Colors.CYAN}
{Colors.GREEN}     _)(  )(_          {Colors.CYAN} Discord ->
{Colors.GREEN}    `---''---`         {Colors.CYAN}     {Colors.UNDERLINE}{Colors.MAGENTA}hirushaadi#8626{Colors.RESET}
    
                  Data Recovery
{Colors.GREY}---------------------------------------------------
   {Colors.RED}THIS TOOL IS FOR DATA RECOVERY PURPOSES ONLY
{Colors.GREY}---------------------------------------------------
          """)
        input(f"{Colors.MAGENTA}Press [ENTER] to Exit{Colors.RESET}")
    sys.exit()


def main():
    parser()

    if args.browser_passwords:
        ChromiumRecovery().run()

    if args.browser_history:
        WebHistoryRecovery().run()

    if args.browser_bookmakrs:
        WebBookmarksRecovery().run()

    if args.network_wifi:
        WifiPasswordRecovery().run()

    if args.network_info:
        NetworkInfoRecovery().run()

    if args.system_all:
        SystemInfoRecovery().run()

    if args.applications_discord:
        DiscordRecovery().run()

    cexit()


if __name__ == "__main__":
    main()
