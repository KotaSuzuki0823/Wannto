#shell coler
class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

def ShowName():
    print('welcome to' + Color.CYAN + '       __                              __           ' + Color.END)
    print(Color.CYAN + '.---.-. .--.--. |  |_  .-----.  .-----. .-----. |  |_  .-----.' + Color.END)
    print(Color.CYAN + '|  _  | |  |  | |   _| |  -__|  |     | |  -  | |   _| |  -__|' + Color.END)
    print(Color.CYAN + '|___._| |_____| |____| |_____|  |__|__| |_____| |____| |_____|' + Color.END)
    print('                                                    By ' + Color.GREEN + 'Wantto \n' + Color.END)


if __name__ == "__main__":
    ShowName()