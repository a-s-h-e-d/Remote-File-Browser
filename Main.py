from gui.Gui import Gui
import time
import sys

app = Gui()

def printSlow(text):
    for char in text:
        print(char, end="")
        sys.stdout.flush()
        time.sleep(.1)
#checking for hwid
'''
def Main():
    if hwid in r.text:
        print("HWID Verified")
        printSlow("Loading GUI.................")
        time.sleep(.1)
        app.mainloop()
    else:
        print("HWID Not Found In Database!")
        print("Please contact me for help. HWID: " + hwid)
        os.system('pause >NUL')

if __name__ == "__main__":
    Main()
'''
app.mainloop()