from tkinter import *
from tkinter.ttk import Progressbar
import subprocess
import speech_recognition as sr
import threading
from PIL import Image, ImageTk
import os

window = Tk()
global image_number
image_number = 0
global letterlist
letterlist = {
        "0":"E",
        "1":"F,P",
        "2":"T,O,Z",
        "3":"L,P,E,D",
        "4":"P,E,C,F,D",
        "5":"E,D,F,C,Z,P",
        "6":"F,E,L,O,P,Z,D",
        "7":"D,E,F,P,O,T,E,C",
    }
global currentletters
currentletters = []

def main():
    window.title("Visual Acuity Voice Recognizer")
    window.attributes('-fullscreen', True) 
    window.configure(bg='#FFFFFF')
    fullScreenState = False
    window.bind("<F11>", toggleFullScreen)
    window.bind("<Escape>", quitFullScreen)
    
    statusText()

    loadallimage()

    global canvas
    canvas = Canvas(window, width = 1920, height = 900, bg='#FFFFFF')  
    canvas.pack() 
    global image_on_canvas
    image_on_canvas = canvas.create_image(1000, 500, anchor=CENTER, image=images[image_number])

    NextButton = Button(window, text ="Next", command=loadimage)
    NextButton.lift(aboveThis=canvas)
    NextButton.pack()

    window.mainloop()

def loadallimage():
    global images
    images = []
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="1.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="2.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="3.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="4.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="5.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="6.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="7.jpg")).replace("\\","/")))
    images.append(ImageTk.PhotoImage(file=("{ospath}\\image\\{file}".format(ospath=os.getcwd(),file="8.jpg")).replace("\\","/")))

def loadimage():
    global image_number
    global currentletters
    global letterlist

    #letters = letterlist.get(image_number)

    # Change to new set of letters
    #for i in letters.split(','):
    #    currentletters.append(i)
    
    if (image_number > 7):
        image_number = 0

    canvas.itemconfig(image_on_canvas, image=images[image_number])

    image_number += 1

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
        textresult = ''
        temp = ''
        while True:
            try:
                r.pause_threshold = 0.8
                r.operation_timeout = None
                audio = r.listen(source, timeout=None)
                textresult = r.recognize_google(audio)
            except sr.RequestError as e:
                print(e)
            except sr.UnknownValueError as eu:
                print(eu)

            #global currentletters
            #if(textresult in currentletters):
                # Avoid reading same letter
            #    currentletters.remove(textresult)
            #    if(currentletters.count == 0):
                    # Empty list of letters means all are done
                    # proceed to next image
            #        loadimage()

            # Proceed if there are changes
            if(textresult == temp):
                continue

            temp = textresult

            message = "you said:{}".format(textresult)
            print(message)

threading.Thread(target=recognizer).start()
main()