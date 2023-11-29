import sys
import argparse


from config import Constant
from config import Colors

from modules import ChromiumRecovery, WebHistoryRecovery, WebBookmarksRecovery  # browser
from modules import NetworkInfoRecovery, WifiPasswordRecovery  # network
from modules import SystemInfoRecovery  # system
from modules import DiscordRecovery, ZipFiles # applications

def parser():
    parser = argparse.ArgumentParser(description="Data Recovery | Built by @hirusha-adi")

    parser.add_argument("--all", "-a", action="store_true", help="Get All Information")

    parser.add_argument("--silent", "-s", action="store_true", help="Silent Mode - No Console Output")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose - Display everything that happens")
    parser.add_argument("--log", "-l", action="store_true", help="Log to file")

    browser_group = parser.add_argument_group("Browser Options")
    browser_group.add_argument("--browser-all", "-ba", action="store_true", help="Get Browser Passwords, Cookies, Cards, History, and Bookmarks")
    browser_group.add_argument("--browser-passwords", "-bp", action="store_true", help="Get Browser Passwords, Cookies, Cards, and History DB File")
    browser_group.add_argument("--browser-history", "-bh", action="store_true", help="Get Browser History")
    browser_group.add_argument("--browser-bookmarks", "-bb", action="store_true", help="Get Browser Bookmarks")

    network_group = parser.add_argument_group("Network Options")
    network_group.add_argument("--network-all", "-na", action="store_true", help="Get All Network Information and Wifi Passwords")
    network_group.add_argument("--network-wifi", "-nw", action="store_true", help="Get Wifi Passwords")
    network_group.add_argument("--network-info", "-ni", action="store_true", help="Get All Network Information")

    system_group = parser.add_argument_group("System Options")
    system_group.add_argument("--system-all", "-sa", action="store_true", help="Get All System Information")

    application_group = parser.add_argument_group("Application Options")
    application_group.add_argument("--apps-all", "-Aa", action="store_true", help="Get Discord Tokens of Logged in Accounts")
    application_group.add_argument("--apps-discord", "-Ad", action="store_true", help="Get Discord Tokens of Logged in Accounts")
    application_group.add_argument("--apps-zip", "-Az", action="store_true", help="Zip and Copy Important Accounts")

    args = parser.parse_args()

    if args.silent and args.verbose:
        parser.error("Only one of --silent or --verbose can be true")

    # set values for args class
    args_values = vars(args)
    for key, value in args_values.items():
        setattr(args, key, value)

    setTrue = lambda *args: [setattr(args, arg, True) for arg in args]

    # conflicts
    if args.all:
        args.browser_all = args.network_all = args.system_all = args.apps_all = True

    if args.browser_all:
        args.browser_passwords = args.browser_history = args.browser_bookmarks = True

    if args.network_all:
        args.network_wifi = args.network_info = True

    # if args_user.system_all:
        # pass 

    if args.apps_all:
        args.apps_discord = args.apps_zip = True

    print(args)
    
    return args

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
    
    args = parser()

    if args.browser_passwords:
        ChromiumRecovery().run()

    if args.browser_history:
        WebHistoryRecovery().run()

    if args.browser_bookmarks:
        WebBookmarksRecovery().run()

    if args.network_wifi:
        WifiPasswordRecovery().run()

    if args.network_info:
        NetworkInfoRecovery().run()

    if args.system_all:
        SystemInfoRecovery().run()

    if args.apps_discord:
        DiscordRecovery().run()
    
    if args.apps_zip:
        ZipFiles().run()

    cexit()


if __name__ == "__main__":
    main()
