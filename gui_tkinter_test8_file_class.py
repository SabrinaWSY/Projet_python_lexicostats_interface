from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror

import langdetect
import re

import jieba
import nltk
from collections import Counter

# --- classes ---

class MyWindow:
    def __init__(self, parent):

        self.parent = parent

        self.filename = None
        self.df = None

        self.text = tk.Text(self.parent)
        self.text.pack()

        # load file button
        self.load_button = tk.Button(self.parent, text='LOAD FILE', command=self.load)
        self.load_button.pack()

        # display path and language button
        self.display_button = tk.Button(self.parent, text='DISPLAY PATH AND LANGUAGE', command=self.display)
        self.display_button.pack()

        # bigram button
        self.bigram_button = tk.Button(self.parent, text='BIGRAMS', command=self.bigram)
        self.bigram_button.pack()

        # run script button
        self.script_button = tk.Button(self.parent, text='RUN SCRIPT', command=self.script_python)
        self.script_button.pack()

        # save data button
        self.save_button = tk.Button(self.parent, text='SAVE DATA', command=self.file_save)
        self.save_button.pack()

    def load(self):
        name = askopenfilename(filetypes=[('TXT', '*.txt',)])
        with open(name,'r') as UseFile:
            self.df = UseFile.read()
            
        self.filename = name

        # display directly
        self.text.insert('end', 'Text preview : \n-----------------\n' + str(self.df)[:300] + '\n--------------------\n')

    def display(self):
        # ask for file if not loaded yet
        if self.df is None:
            self.load_file()

        # display if loaded
        if self.df is not None:
            self.text.insert('end', 'File Path : \n' + self.filename + '\n--------------------\n')
            langs = langdetect.detect_langs(str(self.df))
            language = langs[0]
            #print(language)
            self.text.insert('end', 'Language propability : \n\t' + str(language) + '\n--------------------\n')
            #self.text.insert('end', str(str(self.df)) + '\n')

    def bigram(self):
        # replace this with the real thing
        text = self.df
        textlist = re.sub("[\n]", "", text).split('\.')
        bigrams = [b for l in textlist for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
        res=Counter(bigrams).most_common(len(bigrams))
        print(res)
        self.text.insert('end', 'Bigrams : \n\t' + str(res) + '\n--------------------\n')

    def script_python(self):
        # replace this with the real thing
        self.df = self.df.iloc[:, :-1]

    def file_save(self):
        fname = asksaveasfilename(filetypes=(("txt files", "*.txt"),
                                        ("All files", "*.*")))
        # note: this will fail unless user ends the fname with ".txt"
        with open(fname,'w')as SaveFile:
            SaveFile.write(str(self.df))
            

# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    Title = root.title( "Siyu's Project")
    root.geometry('700x500')
    # add image to the interface
    # canvas = Canvas(width=500, height=300, bg='black')
    # image_file = PhotoImage(file='./bg.gif')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
    # image = canvas.create_image(0, 0, anchor='n',image=image_file)        # 图片锚定点（n图片顶端的中间点位置）放在画布（250,0）坐标处
    # canvas.pack()
    
    top = MyWindow(root)
    root.mainloop()