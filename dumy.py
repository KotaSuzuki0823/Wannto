import welcome as w

def printOK(text):
    print("[" + w.Color.GREEN + "   OK   " + w.Color.END + "]" + text)

def printFATAL(text):
    print("[" + w.Color.RED + "  FATAL " + w.Color.END + "]" + text)


if __name__ == "__main__":
    printOK("test")
    printFATAL("test")