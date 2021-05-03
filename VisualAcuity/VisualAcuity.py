from tkinter import *
from tkinter.ttk import Progressbar

class Fullscreen_Example:
    curtext = "E"
    size = 550

    def __init__(self):
        self.window = Tk()
        self.window.title("Visual Acuity Voice Recognizer")
        self.window.attributes('-fullscreen', True) 
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        self.statusText()
        self.setcurrenttext(Fullscreen_Example.curtext, Fullscreen_Example.size)
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def statusText(self):
        # Create label
        status = Label(self.window, text = "Listening...")
        status.config(font =("Montserrat Semibold", 14))
        status.pack()

        self.showSpinner()

    def setcurrenttext(self,curtext,size):
        currentletter = Label(self.window, text = curtext)
        currentletter.config(font =("Eyechart", size))    
        currentletter.pack(pady=100)

    def showSpinner(self):
        progressbar = Progressbar(self.window,orient=HORIZONTAL,length=200,mode="determinate",takefocus=True,maximum=100)
        progressbar.pack()
        progressbar.start(25)

if __name__ == '__main__':
    app = Fullscreen_Example()
