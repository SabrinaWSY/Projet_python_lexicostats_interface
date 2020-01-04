import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror

import re
import io
import os
import jieba
import jieba.posseg as pseg
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import langdetect
import spacy
from collections import Counter
import pprint   # For proper print of sequences.
import matplotlib
matplotlib.use("TkAgg") 
import matplotlib.pyplot as plt
import numpy as np


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

        # run script button
        self.stats_button = tk.Button(self.parent, text='TOKEN STATS', command=self.token_stats)
        self.stats_button.pack()

        # bigram button
        self.bigram_button = tk.Button(self.parent, text='BIGRAMS', command=self.bigram)
        self.bigram_button.pack()

        self.grapheWindow_button = tk.Button(self.parent, text="POS GRAPHE", command=self.CreateNewWindow)
        self.grapheWindow_button.pack()

        # # save data button
        # self.save_button = tk.Button(self.parent, text='SAVE DATA', command=self.file_save)
        # self.save_button.pack()

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

    def CreateNewWindow(self):
        self.top = tk.Toplevel()
        self.top.title("Graphe Stats")
        

    def bigram(self):
        # create bigrams for non-chinese languages
        text = self.df
        langs = langdetect.detect_langs(text)
        language = str(langs[0])[:2]
        if language == 'zh':
            res = bigram_ch_sort(text)
            #print(res)
            self.text.insert('end', '--------------------\nTop bigrams : \n')
            for b in res[:40]:
                self.text.insert('end', '\t'+ str(b) + '\n')
        else:
            bigram_list = []
            text = re.sub("\n"," ",self.df)
            textlist = re.sub("[(),.]", "", text).split('\.')
            bigrams = [b for l in textlist for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
            #print(bigrams)
            for a in bigrams:
                bigram_list.append(a[0]+' '+a[1])
            res=Counter(bigram_list).most_common(len(bigrams))
            #print(res)
            self.text.insert('end', '--------------------\nTop bigrams : \n')
            for b in res[:40]:
                self.text.insert('end', '\t'+ str(b) + '\n')

    def token_stats(self):
        # tokenize
        text = self.df
        langs = langdetect.detect_langs(text)
        language = str(langs[0])[:2]
        print(language)
        # if chinese
        if language == "zh":
            wordlist_ch = tokenize_ch(text)
            res_ch=Counter(wordlist_ch).most_common(len(wordlist_ch))
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(res_ch[:50]) + '\n')
            list_tag_ch = pos_tag_ch(text)
            self.text.insert('end', '\t'+ str(list_tag_ch) + '\n')
        # if french
        elif language == "fr":
            wordlist_fr = tokenize(self.df, 'french')
            #print(wordlist_fr)
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(wordlist_fr[:50]) + '\n')
            
            tag_fr = nlp_fr(text)
            tag_list = []
            for token in tag_fr:
                print(token.text+"\t"+token.pos_+"\n")
                tag_list.append(token.pos_)
            res=Counter(tag_list).most_common(len(tag_list))
            #print(res)
            self.text.insert('end', '--------------------\nPOS distribution: \n')
            for a in res:
                self.text.insert('end', '\t'+ str(a) + '\n')
            labels, nb = get_value4graph(res)
            tag_bar_graph(labels,nb)
        # if english
        elif language == 'en':
            pass
        # if german
        elif language == 'de': 
            pass
        # if spanish
        # if italien
        else: 
            # text = re.sub("\n"," ",self.df)
            # textlist = re.sub("[(),.]", "", text).split(' ')
            wordlist = word_tokenize(self.df)
            #print(wordlist)
            res=Counter(wordlist).most_common(len(wordlist))
            self.text.insert('end', 'Top tokens : \n')
            self.text.insert('end', '\t'+ str(res[:50]) + '\n')
            pos_list = nltk.pos_tag(wordlist)
            print(pos_list)
            tag_fd = nltk.FreqDist(tag for (word, tag) in pos_list)
            print(tag_fd.most_common())
            for a in tag_fd.most_common():
                self.text.insert('end', '\t'+ str(a) + '\n')

    # def file_save(self):
    #     fname = asksaveasfilename(filetypes=(("txt files", "*.txt"),
    #                                     ("All files", "*.*")))
    #     # note: this will fail unless user ends the fname with ".txt"
    #     with open(fname,'w')as SaveFile:
    #         SaveFile.write(str(self.bigram))
            
def tokenize(text, langue):
    wordlist = word_tokenize(text, language=langue)
    #print(wordlist)
    res=Counter(wordlist).most_common(len(wordlist))
    return res


# tokenize chinese language corpus
def tokenize_ch(text):
	pattern=re.compile(u'[^\u4E00-\u9FA5]')
	text=pattern.sub(r"", text)
	wordlist_temp=list(jieba.cut(text)) # paddle mode
	wordlist=[i.rstrip() for i in wordlist_temp if len(i)>=1]
	return wordlist

def pos_tag_ch(text):
    list_tag_ch = []
    dict_tag_ch = {}
    words = pseg.cut(text,use_paddle=True) # paddle mode
    for word, flag in words:
        dict_tag_ch[word] = flag
        list_tag_ch.append(flag)
        #print(word+flag)
    return list_tag_ch

def bigram_ch(text):
	wordlist=tokenize_ch(text)
	for i in list(nltk.bigrams(wordlist)):
		with io.open('temp.txt','a',encoding='utf-8') as f:
			f.write(i[0]+" "+i[1]+"\n")

def bigram_ch_sort(text):
    bigram_ch(text)
    with io.open('temp.txt','r',encoding='utf-8') as f:
        data=f.readlines()
    res=Counter(data).most_common(len(data))
    os.remove('temp.txt')
    return res
	
# --- graphes ---

def get_value4graph(res):
    labels = []
    nb = []
    for k,v in res:
        labels.append(k)
        nb.append(v)
    return labels, nb

def tag_bar_graph(labels, nb):
    # this is for plotting purpose
    index = np.arange(len(labels))
    plt.bar(index, nb)
    plt.xlabel('Tag', fontsize=5)
    plt.ylabel('Nb', fontsize=5)
    plt.xticks(index, labels, fontsize=5, rotation=30)
    plt.title('Number of each POS')
    plt.show()

# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    Title = root.title( "Siyu's Project")
    root.geometry('800x600')

    nlp_fr = spacy.load('fr_core_news_sm')
    # add image to the interface
    # canvas = Canvas(width=500, height=300, bg='black')
    # image_file = PhotoImage(file='./bg.gif')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
    # image = canvas.create_image(0, 0, anchor='n',image=image_file)        # 图片锚定点（n图片顶端的中间点位置）放在画布（250,0）坐标处
    # canvas.pack()
    
    top = MyWindow(root)
    root.mainloop()