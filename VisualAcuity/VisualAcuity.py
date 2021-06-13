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
import usb.core
import usb.util
import time

global canvas
global status
window = Tk()
global image_set_number
global current_indices
current_indices = []
global current_set_of_images
current_set_of_images = {}
image_set_number = 1
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
        0:"Visual Acuity Score:  Legally blind\n\n",
        1:"Visual Acuity Score:  20/200\n\nEye Refraction: 3.00 to 3.50\n\n",
        2:"Visual Acuity Score:  20/100\n\nEye Refraction: 2.75 to 2.25\n\n",
        3:"Visual Acuity Score:  20/70\n\nEye Refraction: 1.50 to 2.00\n\n",
        4:"Visual Acuity Score:  20/50\n\nEye Refraction: 1.00 to 1.50\n\n",
        5:"Visual Acuity Score:  20/40\n\nEye Refraction: 0.50 to 0.75\n\n",
        6:"Visual Acuity Score:  20/30\n\nEye Refraction: 0.25 to 0.50\n\n",
        7:"Visual Acuity Score:  20/25\n\nEye Refraction: 0.25\n\n",
        8:"Visual Acuity Score:  20/20\n\nEye Refraction: Plano\n\n"
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
    #canvas = Canvas(window, width = 1920, height = 900, bg='#FFFFFF')
    canvas = Canvas(window, width = 1280, height = 720, bg='#FFFFFF')  
    canvas.pack() 
    
    global image_on_canvas
    # X, Y
    image_on_canvas = canvas.create_image(525, 350, anchor=CENTER)

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

# Load all images from all line. Names must be aligned with the jpg file.
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

def debugtest():
    global image_set_number
    global onlefteye
    debugtextresult = ''
    debugtemp = ''
    
    while True:
        debugtextresult = input('text:')
        
        # Will not proceed when there are no speech input
        if debugtextresult == '':
            continue
        message = "you said:{}".format(debugtextresult)
        print(message)
        # Small caps the letters to align with the file name
        debugtextresult = debugtextresult[0].lower()

        global currentletters
        print('letters left:{}'.format(currentletters))
        global picked_letter
        # Speech input compared against random picked letter per line
        if(debugtextresult == picked_letter):
            # Avoid reading same letter by removing the Spoken letter from
            # the loaded set of letters.
            # For ex.
            #       line 2 has a set the contains 'E' and 'D'
            currentletters.remove(debugtextresult)
            print('letters left:{}'.format(currentletters))
            # Empty set/array means next image set will be loaded
            if not currentletters:
                # All lines done
                if image_set_number == 8:
                    if not onlefteye:
                        print('Test all done! Printing result...')
                        status.configure(text="Test all done! Printing result...\n")
                    else:
                        status.configure(text='Done on {}. Printing result...\nTest restarting...'.format(
                           'left eye' if onlefteye else 'right eye'
                        ))

                    printresult()
                    # This will reset the necessary values
                    # to repeat back to the first line
                    reset()
                # Not all lines done proceed to next image set
                else:
                    image_set_number += 1

                print('Loading next image set...')
                prepareimageset()

            shownextimageinset()
        else:
            # Error in test will result printing
            printresult()
            # Already on the right eye. Error means test done.
            if not onlefteye:
                print('Test all done! Printing result...')
                status.configure(text="Test all done! Printing result...\n")
                time.sleep(5)

                status.configure(text="Application closing in 10s.")
                time.sleep(10)

                closewindow()
            else:
                status.configure(text='Done on {}. Printing result...\nTest restarting...'.format(
                   'left eye' if onlefteye else 'right eye'
                ))
            reset()

            prepareimageset()

            shownextimageinset()
        # Proceed if there are changes
        if(debugtextresult == debugtemp):
            continue
        # FOR THE DEV: THIS IS A POSSIBLE BUG
        # scenario:
        #      when line a ended with 'D'
        #      then line b started with 'D'
        debugtemp = debugtextresult
        debugtextresult = ''

def recognizer():   
    global image_set_number
    global onlefteye 
    print('running speech recognition')
    
    with sr.Microphone() as source:
        print('listening...')
        r = sr.Recognizer()
        r.energy_threshold = 4000
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
            
            # Will not proceed when there are no speech input
            if textresult == '':
                continue
            message = "you said:{}".format(textresult)
            print(message)
            # Small caps the letters to align with the file name
            textresult = textresult[0].lower()

            global currentletters
            print('letters left:{}'.format(currentletters))
            global picked_letter
            # Speech input compared against random picked letter per line
            if(textresult == picked_letter):
                # Avoid reading same letter by removing the Spoken letter from
                # the loaded set of letters.
                # For ex.
                #       line 2 has a set the contains 'E' and 'D'
                currentletters.remove(textresult)
                print('letters left:{}'.format(currentletters))
                # Empty set/array means next image set will be loaded
                if not currentletters:
                    # All lines done
                    if image_set_number == 8:
                        if not onlefteye:
                            print('Test all done! Printing result...')
                            status.configure(text="Test all done! Printing result...\n")
                        else:
                            status.configure(text='Done on {}. Printing result...\nTest restarting...'.format(
                               'left eye' if onlefteye else 'right eye'
                            ))

                        printresult()
                        # This will reset the necessary values
                        # to repeat back to the first line
                        reset()
                    # Not all lines done proceed to next image set
                    else:
                        image_set_number += 1

                    print('Loading next image set...')
                    prepareimageset()

                shownextimageinset()
            else:
                # Error in test will result printing
                printresult()
                # Already on the right eye. Error means test done.
                if not onlefteye:
                    print('Test all done! Printing result...')
                    status.configure(text="Test all done! Printing result...\n")
                    time.sleep(5)

                    status.configure(text="Application closing in 5s.")
                    time.sleep(5)

                    closewindow()
                else:
                    status.configure(text='Done on {}. Printing result...\nTest restarting...'.format(
                       'left eye' if onlefteye else 'right eye'
                    ))
                reset()

                prepareimageset()

                shownextimageinset()
            # Proceed if there are changes
            if(textresult == temp):
                continue
            # FOR THE DEV: THIS IS A POSSIBLE BUG
            # scenario:
            #      when line a ended with 'D'
            #      then line b started with 'D'
            temp = textresult
            textresult = ''

# Prepare set of images
# This will resolve the right line and what images
# should be in the line
def prepareimageset():
    global image_set_number
    global currentletters
    global letterlist
    global images
    global current_set_of_images

    if(image_set_number > 8):
        image_set_number -= 1

    print('Current image set number:{}'.format(image_set_number))
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
        
# Load the next image in set randomly.
def shownextimageinset():
    global picked_letter
    picked_letter = random.choice(currentletters)
    
    global canvas
    canvas.itemconfig(image_on_canvas, image=current_set_of_images[picked_letter])

def reset():
    global status
    global onlefteye
    global image_set_number
    global currentletters

    # Sleep the app to have time to
    # see the prompt
    time.sleep(5)     

    status.configure(text="listening...") 

    # Error in test means first eye done.
    # right eye next
    onlefteye = not onlefteye

    # Will reset the set of images back to first set
    image_set_number = 0
    image_set_number += 1
                
    # Avoid unnecessary letters
    currentletters.clear()

def printresult():
    global image_set_number
    global onlefteye
    global score

    # Xprinter[vendorid, productid, 0, in, out]
    # Identified thru lsusb
    p = Usb(0x0483, 0x070b, 0, 0x81, 0x02)
    p.text('DIROY ~ ROSEUS\n\nOPTICAL CLINIC\n\n(+63917 142 9401)\n\n\n{}'.format('Left eye result\n' if onlefteye else 'Right eye result\n'))
    #print('{}'.format('Left eye result' if onlefteye else 'Right eye result'))
    p.set(align='center')
    print('current image set number:{}'.format(image_set_number))

    if(image_set_number == 8):   
        p.text(score.get(image_set_number))
    else:
        # Print the score. (-1) to get the score where the user had mistake
        p.text(score.get(image_set_number - 1))
    
    if image_set_number == 1:
        # First line error means blind
        image_set_number = 0
    print(score.get(image_set_number))
    p.set(align='center')
    p.text('Your Visual Acuity test has been completed. Thank You!')
    p.set(align='center')

    # Cut paper
    p.cut()

    # Avoid resource busy
    dev = usb.core.find(idVendor=0x0483, idProduct=0x070b)
    dev.reset()
                

thread = threading.Thread(target=recognizer)
#thread = threading.Thread(target=debugtest)
thread.setDaemon(True)
thread.start()
main()