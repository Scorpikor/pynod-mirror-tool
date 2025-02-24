# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

class TColor:
    # use: print t_color.RED + str("TEXT") + t_color.ENDC
    GRAY = str("\033[1;30m")
    RED = str("\033[1;31m")
    GREEN = str("\033[1;32m")
    YELLO = str("\033[1;33m")
    BLUE = str("\033[1;34m")
    MAGENTA = str("\033[1;35m")
    CYAN = str("\033[1;36m")
    WHITE = str("\033[1;37m")
    CRIMSON = str("\033[1;38m")
    ENDC = str("\033[0m")
    BOLD = str("\033[1m")
    LINE = str("=" * 70)
    UNDERLINE = str("\033[4m")