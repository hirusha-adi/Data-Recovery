# Special thanks to:
#   https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

import os
import sys

class Colors:
    """ANSI color codes, disabled if the terminal does not support colors."""
    
    # Detect if the terminal supports ANSI colors
    _SUPPORTS_COLOR = sys.stdout.isatty() and (os.name != "nt" or "WT_SESSION" in os.environ or "TERM" in os.environ)

    BLACK = '\033[30m' if _SUPPORTS_COLOR else ''
    RED = '\033[31m' if _SUPPORTS_COLOR else ''
    GREEN = '\033[32m' if _SUPPORTS_COLOR else ''
    YELLOW = '\033[33m' if _SUPPORTS_COLOR else ''
    BLUE = '\033[34m' if _SUPPORTS_COLOR else ''
    MAGENTA = '\033[35m' if _SUPPORTS_COLOR else ''
    CYAN = '\033[36m' if _SUPPORTS_COLOR else ''
    WHITE = '\033[37m' if _SUPPORTS_COLOR else ''
    GREY = '\33[90m' if _SUPPORTS_COLOR else ''
    UNDERLINE = '\033[4m' if _SUPPORTS_COLOR else ''
    RESET = '\033[0m' if _SUPPORTS_COLOR else ''
