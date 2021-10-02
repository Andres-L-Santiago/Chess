class Colors:

    # General Modifiers

    reset = '\033[0m'
    bold = '\x1b[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:

        # General Foreground Colors

        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
        white = '\u001b[37m'

        # Dimmed Foreground Colors

        IBlack = "\033[0;90m"
        IRed = "\033[0;91m"
        IGreen = "\033[0;92m"
        IYellow = "\033[0;93m"
        IBlue = "\033[0;94m"
        IPurple = "\033[0;95m"
        ICyan = "\033[0;96m"
        IWhite = "\033[0;97m"

        # Chess Foreground Colors (USE THESE)

        Light_Ch = '\x1b[38;5;15m'
        Dark_Ch = '\x1b[38;5;16m'

    class bg:

        # General Background Colors

        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

        # Dimmed Background Colors

        On_IBlack = "\033[0;100m"
        On_IRed = "\033[0;101m"
        On_IGreen = "\033[0;102m"
        On_IYellow = "\033[0;103m"
        On_IBlue = "\033[0;104m"
        On_IPurple = "\033[10;95m"
        On_ICyan = "\033[0;106m"
        On_IWhite = "\033[0;107m"

        # Chess Backgrounds (USE THESE)

        Light_Ch = '\x1b[48;5;138m'  # 216 for different tan
        Dark_Ch = '\x1b[48;5;95m'  # 173 for different brown
