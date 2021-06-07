from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
import subprocess
import speech_recognition as sr
import threading
from PIL import Image, ImageTk
import os
import sys
import random
from escpos.printer import Usb

global canvas
global status
window = Tk()
global image_set_number
global current_indices
current_indices = []
global current_set_of_images
current_set_of_images = {}
image_set_number = 7
global letterlist
letterlist = {
        1:["F"],
        2:['E','D'],
        3:['C','O','D'],
        4:['Z','D','P'],
        5:['E','C','O','F'],
        6:['P','X','Y','H','E'],
        7:['D','F','Z','C','P','E'],
        8:['O','D','L','Z','X','F','Y'],
    }
global score
score = {
        1:"Visual Acuity Score: 20/200\n\nEye Refraction: 3.00 to 3.50\n\n",
        2:"Visual Acuity Score: 20/100\n\nEye Refraction: 2.75 to 2.25\n\n",
        3:"Visual Acuity Score: 20/70\n\nEye Refraction: 1.50 to 2.00\n\n",
        4:"Visual Acuity Score: 20/50\n\nEye Refraction: 1.00 to 1.50\n\n",
        5:"Visual Acuity Score: 20/40\n\nEye Refraction: 0.50 to 0.75\n\n",
        6:"Visual Acuity Score: 20/30\n\nEye Refraction: 0.25 to 0.50\n\n",
        7:"Visual Acuity Score: 20/25\n\nEye Refraction: 0.25\n\n",
        8:"Visual Acuity Score: 20/20\n\nEye Refraction: Plano\n\n"
    }
global currentletters
currentletters = []

# Will always start at left eye
global onlefteye
onlefteye = True

global picked_letter
picked_letter = ''

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
    image_on_canvas = canvas.create_image(1000, 500, anchor=CENTER)

    prepareimageset()

    shownextimageinset()

    ExitButton = Button(window, text="Exit", command=closewindow, height=2, width=5)
    ExitButton.lift(aboveThis=canvas)
    ExitButton.pack()

    NextButton = Button(window, text ="Next", command=prepareimageset)
    NextButton.place(x=100, y=100)
    NextButton.lift(aboveThis=canvas)
    NextButton.pack()

    NextButton.pack_forget()

    window.mainloop()

def closewindow():
    window.destroy()

def loadallimage():
    global images
    images = {
        1:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_1\\{file}".format(ospath=os.getcwd(),file="f.jpg")).replace("\\","/"))
        ],
        2:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_2\\{file}".format(ospath=os.getcwd(),file="e.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_2\\{file}".format(ospath=os.getcwd(),file="d.jpg")).replace("\\","/"))
        ],
        3:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_3\\{file}".format(ospath=os.getcwd(),file="c.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_3\\{file}".format(ospath=os.getcwd(),file="o.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_3\\{file}".format(ospath=os.getcwd(),file="d.jpg")).replace("\\","/"))
        ],
        4:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_4\\{file}".format(ospath=os.getcwd(),file="z.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_4\\{file}".format(ospath=os.getcwd(),file="d.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_4\\{file}".format(ospath=os.getcwd(),file="p.jpg")).replace("\\","/"))
        ],
        5:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_5\\{file}".format(ospath=os.getcwd(),file="e.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_5\\{file}".format(ospath=os.getcwd(),file="c.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_5\\{file}".format(ospath=os.getcwd(),file="o.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_5\\{file}".format(ospath=os.getcwd(),file="f.jpg")).replace("\\","/"))
        ],
        6:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_6\\{file}".format(ospath=os.getcwd(),file="p.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_6\\{file}".format(ospath=os.getcwd(),file="x.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_6\\{file}".format(ospath=os.getcwd(),file="y.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_6\\{file}".format(ospath=os.getcwd(),file="h.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_6\\{file}".format(ospath=os.getcwd(),file="e.jpg")).replace("\\","/"))
        ],
        7:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_7\\{file}".format(ospath=os.getcwd(),file="d.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_7\\{file}".format(ospath=os.getcwd(),file="f.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_7\\{file}".format(ospath=os.getcwd(),file="z.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_7\\{file}".format(ospath=os.getcwd(),file="c.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_7\\{file}".format(ospath=os.getcwd(),file="p.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_7\\{file}".format(ospath=os.getcwd(),file="e.jpg")).replace("\\","/"))
        ],
        8:[
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="o.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="d.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="l.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="z.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="x.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="f.jpg")).replace("\\","/")),
            ImageTk.PhotoImage(file=("{ospath}\\image\\line_8\\{file}".format(ospath=os.getcwd(),file="y.jpg")).replace("\\","/")),
        ]
    }

# Prepare set of images
def prepareimageset():
    global image_set_number
    global currentletters
    global letterlist
    global images
    global current_set_of_images

    letters = letterlist.get(image_set_number)

    # Change to new array of letters
    for idx,item in enumerate(letters, start=0):
        currentletters.insert(idx, item.lower())

    # Prepare fetched set of images into key(letter)-value(.jpg) pair
    for idx,item in enumerate(images, start=0):
        current_set_of_images[currentletters[idx]] = images.get(image_set_number)[idx]
        # We only need set of image at a time
        if (idx == len(currentletters) - 1):
            break
    
    if (image_set_number > 8):
        image_set_number = 1
        return
        
    image_set_number += 1

def shownextimageinset():
    # Load the next image in set randomly.
    # Avoid repeating image
    global picked_letter
    picked_letter = random.choice(currentletters)
    
    global canvas
    canvas.itemconfig(image_on_canvas, image=current_set_of_images[picked_letter])

def toggleFullScreen(event):
    fullScreenState = not fullScreenState
    window.attributes("-fullscreen", fullScreenState)

def quitFullScreen(event):
    fullScreenState = False
    window.attributes("-fullscreen", fullScreenState)

def statusText():
    # Create label
    global status
    status = Label(window, text = "listening...", bg="#FFFFFF")
    status.config(font =("Montserrat Semibold", 14))
    status.pack()

def recognizer():
    global image_set_number
    global picked_letter
    
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

            textresult = textresult[0].lower()

            # Accept only first index 
            if(textresult == picked_letter):
                # Avoid reading same letter
                currentletters.remove(textresult)
                print('letters left:{}'.format(currentletters))
                if not currentletters:
                   # Empty list of letters means all are done
                   # proceed to next set of images
                   print('loading next image...')
                   prepareimageset()
                   
                shownextimageinset()
            elif(textresult != currentletters or image_set_number > 8): #image_set_number > 8 means test finished
                global score
                global letterlist
                global letters
                global onlefteye

                print('printing result...\n')
                
                # Xprinter[vendorid, productid, 0, in, out]
                # Identified thru lsusb
                p = Usb(0x0483, 0x070b, 0, 0x81, 0x02)
                p.text('DIROY ~ ROSEUS\n\nOPTICAL CLINIC\n\n(+63917 142 9401)\n\n\n{}'.format('Left eye result' if onlefteye else 'Right eye result'))
                p.set(align='center')
                p.text(score.get(image_set_number))
                p.set(align='center')
                p.text('Your Visual Acuity test has been completed. Thank You!')
                p.set(align='center')
                
                # Cut paper
                p.cut()

                # Will reset the set of images back to first set
                image_set_number = 1
                
                # Avoid unnecessary letters
                currentletters.clear()

                global status
                status.configure(text="Done. Printing result...\nTest restarted")

                prepareimageset()
                
                shownextimageinset()
                
                # Error in test means first eye done.
                # right eye next
                onlefteye = False    
            
            message = "you said:{}".format(textresult)
            print(message)

            # Proceed if there are changes
            if(textresult == temp):
                continue

            temp = textresult
            textresult = ''

thread = threading.Thread(target=recognizer)
thread.setDaemon(True)
thread.start()
main()
