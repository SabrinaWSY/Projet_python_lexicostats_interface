import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
import pandas as pd

import csv

# --- classes ---

class MyWindow:
    def __init__(self, parent):

        self.parent = parent

        self.filename = None
        self.df = None

        self.text = tk.Text(self.parent)
        self.text.pack()

        # load data button
        self.load_button = tk.Button(self.parent, text='LOAD DATA', command=self.load)
        self.load_button.pack()

        # display data button
        self.display_button = tk.Button(self.parent, text='DISPLAY DATA', command=self.display)
        self.display_button.pack()

        # run script button
        self.script_button = tk.Button(self.parent, text='RUN SCRIPT', command=self.script_python)
        self.script_button.pack()

        # save data button
        self.save_button = tk.Button(self.parent, text='SAVE DATA', command=self.file_save)
        self.save_button.pack()

    def load(self):
        name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xslm', '*.xlsx'))])

        if name:
            if name.endswith('.csv'):
                self.df = pd.read_csv(name)
            else:
                self.df = pd.read_excel(name)

            self.filename = name

            # display directly
            self.text.insert('end', str(self.df.head()) + '\n')

    def display(self):
        # ask for file if not loaded yet
        if self.df is None:
            self.load_file()

        # display if loaded
        if self.df is not None:
            self.text.insert('end', self.filename + '\n')
            self.text.insert('end', str(self.df.head()) + '\n')

    def script_python(self):
        # replace this with the real thing
        self.df = self.df.iloc[:, :-1]

    def file_save(self):
        fname = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                        ("All files", "*.*")))
        # note: this will fail unless user ends the fname with ".xlsx"
        self.df.to_excel(fname)


# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    top = MyWindow(root)
    root.mainloop()