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
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import langdetect
import spacy
import matplotlib
matplotlib.use("TkAgg") 
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
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

        # run script button
        self.stats_button = tk.Button(self.parent, text='TOKEN STATS', command=self.token_stats)
        self.stats_button.pack()

        # bigram button
        self.bigram_button = tk.Button(self.parent, text='BIGRAMS', command=self.bigram)
        self.bigram_button.pack()

        self.grapheWindow_button = tk.Button(self.parent, text="WORDCLOUD", command=self.wordcloud_graph)
        self.grapheWindow_button.pack()


    def load(self):
        self.text.delete('1.0','end')
        name = askopenfilename(filetypes=[('TXT', '*.txt',)])
        with open(name,'r') as UseFile:
            self.df = UseFile.read()
            
        self.filename = name

        # display directly
        self.text.insert('end', '--------------------\nText preview : \n-----------------\n' + str(self.df)[:300] +'\n')

    def display(self):
        # ask for file if not loaded yet
        if self.df is None:
            tk.messagebox.showinfo('Warning','No file loaded!')

        # display if loaded
        if self.df is not None:
            self.text.insert('end', '\n--------------------\nFile Path : \n' + self.filename)
            langs = langdetect.detect_langs(str(self.df))
            language = langs[0]
            #print(language)
            self.text.insert('end', '\n--------------------\nLanguage propability : \n\t' + str(language)+'\n')

    def wordcloud_graph(self):
        if self.df is None:
            tk.messagebox.showinfo('Warning','No file loaded!')
        
        text = self.df
        langs = langdetect.detect_langs(text)
        language = str(langs[0])[:2]
        if language == 'zh':
            font = './simfang.ttf'
            wc = WordCloud(font_path=font, background_color="white", max_words=2000,
               max_font_size=100, random_state=42, width=1000, height=860, margin=2,).generate(jieba_processing_txt(text))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()
        elif language == 'en':
            stop_words = stopwords.words('english')
            generate_wordcloud(text, stop_words)
        elif language == 'fr':
            stop_words = stopwords.words('french')
            temp_words = ["les", "une", "cette", "elle","c'est"]
            for i in temp_words:
                stop_words.append(i)
            generate_wordcloud(text, stop_words)
        elif language == 'de':
            stop_words = stopwords.words('german')
            generate_wordcloud(text, stop_words)
        elif language == 'es':
            stop_words = stopwords.words('spanish')
            generate_wordcloud(text, stop_words)
        elif language == 'it':
            stop_words = stopwords.words('italian')
            generate_wordcloud(text, stop_words)
        else:
            self.text.insert('end', 'Sorry, other languages not supported yet...')

    def bigram(self):
        if self.df is None:
            tk.messagebox.showinfo('Warning','No file loaded!')

        # create bigrams for non-chinese languages
        text = self.df
        langs = langdetect.detect_langs(text)
        language = str(langs[0])[:2]

        # if chinese
        if language == 'zh':
            res = bigram_ch_sort(text)
            #print(res)
            self.text.insert('end', '--------------------\nTop bigrams : \n')
            for b in res[:40]:
                self.text.insert('end', '\t'+ str(b) + '\n')

        # other languages (separated by space)
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
        if self.df is None:
            tk.messagebox.showinfo('Warning','No file loaded!')

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
            res_tag_ch = Counter(list_tag_ch).most_common(len(list_tag_ch))
            self.text.insert('end', '--------------------\nPOS distribution: \n')
            for a in res_tag_ch:
                self.text.insert('end', '\t'+ str(a) + '\n')
            # graph
            labels,nb = get_value4graph(res_tag_ch)
            tag_bar_graph(labels,nb)

        # if french
        elif language == "fr":
            wordlist_fr = tokenize(self.df, 'french')
            #print(wordlist_fr)
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(wordlist_fr[:50]) + '\n')
            tag_fr = nlp_fr(text)
            process_occi(text,tag_fr,self)

        # if english
        elif language == 'en':
            wordlist_en = word_tokenize(self.df,'english')
            #print(wordlist_en)
            res=Counter(wordlist_en).most_common(len(wordlist_en))
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(res[:50]) + '\n')
            pos_list = nltk.pos_tag(wordlist_en)
            #print(pos_list)
            tag_fd = nltk.FreqDist(tag for (word, tag) in pos_list)
            print(tag_fd.most_common())
            self.text.insert('end', '--------------------\nPOS distribution: \n')
            for a in tag_fd.most_common():
                self.text.insert('end', '\t'+ str(a) + '\n')
            # graph
            labels, nb = get_value4graph(tag_fd.most_common())
            tag_bar_graph(labels,nb)

        # if german
        elif language == 'de': 
            wordlist_de = tokenize(self.df, 'german')
            #print(wordlist_de)
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(wordlist_de[:50]) + '\n')
            tag_de = nlp_de(text)
            process_occi(text,tag_de,self)

        # if spanish
        elif language == 'es': 
            wordlist_es= tokenize(self.df, 'spanish')
            #print(wordlist_es)
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(wordlist_es[:50]) + '\n')
            tag_es = nlp_es(text)
            process_occi(text,tag_es,self)

        # if italien
        elif language == 'it': 
            wordlist_it= tokenize(self.df, 'spanish')
            #print(wordlist_it)
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(wordlist_it[:50]) + '\n')
            tag_it = nlp_it(text)
            process_occi(text,tag_it,self)

        # other languages are considered as english treatement rules
        else: 
            wordlist = word_tokenize(self.df)
            #print(wordlist)
            res=Counter(wordlist).most_common(len(wordlist))
            self.text.insert('end', '--------------------\nTop tokens : \n')
            self.text.insert('end', '\t'+ str(res[:50]) + '\n')
            pos_list = nltk.pos_tag(wordlist)
            print(pos_list)
            tag_fd = nltk.FreqDist(tag for (word, tag) in pos_list)
            print(tag_fd.most_common())
            self.text.insert('end', '--------------------\nPOS distribution: \n')
            for a in tag_fd.most_common():
                self.text.insert('end', '\t'+ str(a) + '\n')


# --- for occidental language corpus ---
def tokenize(text, langue):
    wordlist = word_tokenize(text, language=langue)
    #print(wordlist)
    res=Counter(wordlist).most_common(len(wordlist))
    return res

def process_occi(text,tag_lang,self):
    tag_list = []
    for token in tag_lang:
        print(token.text+"\t"+token.pos_+"\n")
        tag_list.append(token.pos_)
    res=Counter(tag_list).most_common(len(tag_list))
    #print(res)
    self.text.insert('end', '--------------------\nPOS distribution: \n')
    for a in res:
        self.text.insert('end', '\t'+ str(a) + '\n')
    # graph
    labels, nb = get_value4graph(res)
    tag_bar_graph(labels,nb)

def generate_wordcloud(text,stop_words):
    # Create and generate a word cloud image:
    # lower max_font_size, change the maximum number of word and lighten the background:
    wordcloud = WordCloud(stopwords = stop_words, background_color="white", max_words=2000,
       max_font_size=100, random_state=42, width=1000, height=860, margin=2).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# --- for chinese corpus ---
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

# The function for processing text with Jieba
def jieba_processing_txt(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)

    for myword in liststr.split('/'):
        if len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)

	
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

# to add : wordcloud


# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    Title = root.title( "POStats Interface")
    root.geometry('800x550')

    nlp_fr = spacy.load('fr_core_news_sm')
    nlp_de = spacy.load('de_core_news_sm')
    nlp_es = spacy.load('es_core_news_sm')
    nlp_it = spacy.load('it_core_news_sm')
    
    top = MyWindow(root)
    root.mainloop()