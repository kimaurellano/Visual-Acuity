from tkinter import *
from tkinter.ttk import Progressbar
import subprocess
import speech_recognition as sr
import threading

curtext = 'E'
size = 550
window = Tk()

def main():
    window.title("Visual Acuity Voice Recognizer")
    window.attributes('-fullscreen', True) 
    fullScreenState = False
    window.bind("<F11>", toggleFullScreen)
    window.bind("<Escape>", quitFullScreen)
    
    statusText()
    setcurrenttext(curtext, size)
    window.mainloop()

def toggleFullScreen(event):
    fullScreenState = not fullScreenState
    window.attributes("-fullscreen", fullScreenState)

def quitFullScreen(event):
    fullScreenState = False
    window.attributes("-fullscreen", fullScreenState)

def statusText():
    # Create label
    status = Label(window, text = "Listening...")
    status.config(font =("Montserrat Semibold", 14))
    status.pack()

    showSpinner()

def setcurrenttext(curtext,size):
    currentletter = Label(window, text = curtext)
    currentletter.config(font =("Eyechart", size))    
    currentletter.pack(pady=100)

def showSpinner():
    progressbar = Progressbar(window,orient=HORIZONTAL,length=200,mode="determinate",takefocus=True,maximum=100)
    progressbar.pack() 
    progressbar.start(25)   

def recognizer():
    print('running speech recognition')
    
    r = sr.Recognizer()
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print('listening...')
        audio = r.listen(source)
        temp = ''
        while True:
            try:
                textresult = r.recognize_google(audio)

                # Proceed if there are changes
                if(textresult == temp):
                    continue

                temp = textresult

                message = "you said:{}".format(textresult)
                print(message)

                audio = r.listen(source)
            except:
               print('can you say it louder?')
    

threading.Thread(target=recognizer).start()
# main()