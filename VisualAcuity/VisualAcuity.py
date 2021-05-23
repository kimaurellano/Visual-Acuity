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
        0:"F",
        1:"E,D",
        2:"C,O,D",
        3:"Z,D,P",
        4:"E,C,O,F",
        5:"P,X,Y,H,E",
        6:"D,F,Z,C,P,E",
        7:"O,D,L,Z,X,F,Y",
    }
global score
score = {
        0:"3.00 to 3.50",
        1:"2.75 to 2.25",
        2:"1.50 to 2.00",
        3:"1.00 to 1.50",
        4:"0.50 to 0.75",
        5:"0.25 to 0.50",
        6:"0.25",
        7:"Plano",
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

    loadimage()

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

    letters = letterlist.get(image_number)

    # Change to new set of letters
    for i in letters.split(','):
        currentletters.append(i)
    
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

            global currentletters
            if textresult == '':
                continue

            textresult = textresult[0].upper()

            # Accept only first index letters
            if(textresult in currentletters):
               # Avoid reading same letter
                currentletters.remove(textresult)
                print('letters left:{}'.format(currentletters))
                if not currentletters:
                   # Empty list of letters means all are done
                   # proceed to next image
                   print('loading next image...')
                   loadimage()
            elif(textresult not in currentletters):
                global score
                global image_number
                global letterlist
                global letters

                print('printing result\n{}\nResetting to '.format(score[image_number]))
                
                # Reset values to first
                image_number = 0
                letters = letterlist.get(image_number)
                
                # Avoid unnecessary letters
                currentletters.clear()

                # Change back to first set of letters
                for i in letters.split(','):
                    currentletters.append(i)
                print(currentletters)
                
            message = "you said:{}".format(textresult)
            print(message)

            # Proceed if there are changes
            if(textresult == temp):
                continue

            temp = textresult
            textresult = ''

threading.Thread(target=recognizer).start()
main()