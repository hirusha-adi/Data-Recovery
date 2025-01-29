import sys
from config import Colors, Constant


class Messages:
    @staticmethod
    def cexit():
        if not (Constant.Args.silent):
            print(
                f"""
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
        """
            )
            input(f"{Colors.MAGENTA}Press [ENTER] to Exit{Colors.RESET}")
        sys.exit()
