#! Python 3.6
# -*- coding: utf-8 -*-
# 4nd test of tkinter gui interface
"""
Open a file dialog window in tkinter using the filedialog method.
Tkinter has a prebuilt dialog window to access files. 
This example is designed to show how you might use a file dialog askopenfilename
and use it in a program.
"""

from tkinter import *
from tkinter import ttk

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import langdetect

root = Tk(  )
#text_display = Tk(  )
langue = []
text_input = []
#This is where we lauch the file manager bar.
def OpenFile():
    global text_input
    name = askopenfilename(initialdir="/Users/*/*",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as UseFile:
            text = UseFile.read()
            langs = langdetect.detect_langs(text)
            new_winF(text,"Text preview")
            #btn_text = ttk.Button(root, text='Show Text', command=show_text(text))
            #btn_text.place(x=220, y=240)
            text_input.append(text)
            print(text)
            language = langs[0]
            #for language in langs:
            print(language)
            btn_show_lang = ttk.Button(root, text='Show info', command=popup_langinfo(language))
            btn_show_lang.place(x=400, y=240)
            btn_show_lang.mainloop()
    except:
        print("No file exists")

def processText(text):
    pass

def new_winF(text,title): # new window definition
    newwin = Toplevel(root)
    Title = newwin.title(title)
    display = Label(newwin, text=text)
    display.pack()   

def show_text(text_input):
    win = Toplevel(root)
    win.wm_title("Text preview")

    l = Label(win, text=text_input)
    l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

def popup_langinfo(language):
    showinfo("Language", language)


Title = root.title( "Siyu's Project")
root.geometry('700x500')
canvas = Canvas(width=700, height=500, bg='black')

image_file = PhotoImage(file='./bg.gif')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
image = canvas.create_image(0, 0, anchor='n',image=image_file)        # 图片锚定点（n图片顶端的中间点位置）放在画布（250,0）坐标处
canvas.pack()
label = ttk.Label(root, text ="I can open a file now!!!",foreground="black",font=("Helvetica", 20))
label.pack()


#Menu Bar
menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = lambda:exit())

menu.add_cascade(label = 'File', menu = file)
menu.add_cascade(label = 'Help')

print(text_input)
#print(langue)
# T = Text(text_display, height=2, width=30)
# T.pack()
# T.insert(END, text_input)
# text_display.mainloop()

root.mainloop()
