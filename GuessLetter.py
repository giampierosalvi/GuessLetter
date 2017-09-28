from __future__ import division
from Tkinter import *
from functools import partial
import string
import random
#import Tkinter.ttk as ttk
#from tkinter import font
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.stats import multivariate_normal
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.colors import LogNorm
#from tkinter import messagebox

class GuessLetter():
    """Guess Letter Class"""
    def __init__(self, tkWindow):
        # variables
        self.guessedText = StringVar()
        self.guessedText.set('*')
        self.charIdx=0
        self.nGuesses = 0
        self.entropyStr = StringVar()
        # this should be read from file
        self.sentences = [
            'in his silk pajamas and smoking jacket',
            'for years republican lawmakers lamented the soaring national debt pressing for spending cuts and clinging to the mantle of fiscal responsibility'
        ]
        self.usedSentences = []
        self.mainWindow = tkWindow
        self.mainWindow.title('GuessLetter')
        self.mainWindow.geometry("960x250")
        self.mainWindow.resizable(1,1)
        self.textFrame = Frame(self.mainWindow)
        self.textDisplay = Entry(self.textFrame, textvariable=self.guessedText)
        self.textDisplay.pack(fill=BOTH, expand=1)
        self.textFrame.pack(fill=BOTH, expand=1)
        self.letterFrame = Frame(self.mainWindow)
        self.alphabeth = list(string.ascii_lowercase)
        self.options = ['space'] + self.alphabeth
        self.entropyTerms = np.array([])
        self.updateEntropy(1.0/len(self.options))
        #self.buttons = []
        self.ch2button = {}
        for opt in self.options:
            button = Button(self.letterFrame, text = opt, command = partial(self.guessLetter, opt))
            button.pack(side=LEFT)
            if opt=='space':
                key='<space>'
                ch=' '
            else:
                key = opt
                ch = opt
            self.ch2button[ch] = button
            self.mainWindow.bind(key, self.guessLetter) # needs arg
            #self.buttons.append(button)
        self.letterFrame.pack(expand=1)
        self.controlsFrame = Frame(self.mainWindow)
        self.newSentenceButton = Button(self.controlsFrame, text = 'new sentence', command = self.chooseNewSentence)
        self.entropyLabel = Label(self.controlsFrame, text="Entropy:")
        self.entropyDisplay = Entry(self.controlsFrame, textvariable=self.entropyStr)
        self.newSentenceButton.pack(side=LEFT)
        self.entropyLabel.pack(side=LEFT)
        self.entropyDisplay.pack(side=LEFT)
        self.controlsFrame.pack(expand=1)
        self.chooseNewSentence()
    def resetButtons(self, event=None):
        for button in self.ch2button.values():
            button.configure(state=NORMAL)
    def disableButtons(self, event=None):
        for button in self.ch2button.values():
            button.configure(state=DISABLED)
    def updateEntropy(self, prob):
        self.entropyTerms = np.append(self.entropyTerms, -prob * np.log2(prob))
        self.entropyStr.set(str(self.entropyTerms.mean()))
    def guessLetter(self, event=None):
        if isinstance(event, basestring):
            ch = event
            if ch == 'space':
                ch = ' '
        else:
            ch = event.char
        self.nGuesses = self.nGuesses+1
        sentence = self.sentences[self.currentSentence]
        print('current character:', sentence[self.charIdx])
        print('guessing:', ch)
        if ch==sentence[self.charIdx]:
            print('correct!')
            self.updateEntropy(self.nGuesses/len(self.options))
            self.charIdx = self.charIdx + 1
            self.guessedText.set(sentence[0:self.charIdx]+'*')
            if self.charIdx == len(sentence):
                self.disableButtons()
            else:
                self.resetButtons()
        else:
            self.ch2button[ch].configure(state=DISABLED)
        return 0
    def chooseNewSentence(self, event=None):
        allSentences = list(range(len(self.sentences)))
        unusedSentences = list(set(allSentences)-set(self.usedSentences))
        self.currentSentence = random.choice(unusedSentences)
        self.usedSentences.append(self.currentSentence)
        self.resetButtons()
        self.entropyTerms = np.array([])
        self.updateEntropy(1.0/len(self.options))
        self.charIdx = 0
        self.guessedText.set('*')


root = Tk()
game = GuessLetter(root)
root.mainloop()
