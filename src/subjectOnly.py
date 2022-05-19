import logging
import random
import sys
import time

import os
import time
import datetime
import numpy as np
import pygame
from time import sleep
from googletrans import Translator
import threading
import continuous_threading
import queue
from gtts import gTTS
from mutagen.mp3 import MP3
from playsound import playsound

import pyglet
import sys
import defines.speakandrecognize as snr
import speech_recognition as sr
import arduinoServo as ard
import PyQt5.QtCore
import PyQt5

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import *

translator= Translator()

pygame.mixer.init()
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
logging.basicConfig(format="%(message)s", level=logging.INFO)

global activeScreen, speaking, duration, flag, subjectLesson, user_input, score
score = 0
duration = 0
user_input = ""
subjectLesson = ""
my_answer = ""
language = ""
counter = 0
p = 0
activeScreen = ""
translatedWord = ""
r = sr.Recognizer()
m = sr.Microphone()
speaking = False
flag = ""

import sys
from time import sleep

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# function to convert the seconds into readable format
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600

    mins = seconds // 60
    seconds %= 60

    return hours, mins, seconds

def speak(text, lang="en"):  # here audio is var which contain text
    # Call LED lights here
    speaking = True
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    playsound(filename, False)
    # Create an MP3 object
    # Specify the directory address to the mp3 file as a parameter
    audio = MP3("temp.mp3")
    # Contains all the metadata about the mp3 file
    audio_info = audio.info    
    length_in_secs = int(audio_info.length)
    hours, mins, seconds = convert(length_in_secs)
    sleep(seconds+0.7)

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    
    def subjectNow(self):
        #speaks(self.script)
        #self.updateScreen(subject)
        #speaks("Try to read the sets of words below")
        self.progress.emit("In this lesson, you will learn about Rhyming Words.")
        speak("In this lesson, you will learn about Rhyming Words.")
        self.progress.emit("Words are formed by combining the letters of the alphabet.")
        speak("Words are formed by combining the letters of the alphabet.")
        self.progress.emit("It is important to remember that the English alphabet is composed of 26 letters with 5 vowels and 21 consonants.")
        speak("It is important to remember that the English alphabet is composed of 26 letters, with 5 vowels and 21 consonants.")
        self.progress.emit("Vowels: \nAa  Ee Ii Oo Uu")
        speak("vowels are like, ah. ae. ē. oh. oooh.")
        self.progress.emit("Consonants: \nBb Cc Dd Ff Gg Hh Jj Kk Ll Mm Nn Pp Qq Rr Ss Tt Vv Ww Xx Yy Zz.")
        speak("Now, consonants are like alphabets without vowels. Such as b,c,d,f,g, and so on.")
        self.progress.emit("By combining some of these letters, words may be formed.")
        speak("By combining some of these letters, words may be formed.")
        self.progress.emit("Some of these words include net, one, pen, and red. Some words have the same or similar ending sounds.")
        speak("Some of these words include net, one, pen, and red.Some words have the same or similar ending sounds.")
        self.progress.emit("They are called rhyming words.At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        speak("They are called rhyming words.At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        self.progress.emit("SET A: \nHouse - Mouse.")
        speak("Try to read the example below.")
        
        while True:
            response = ask_ettibot().lower()     
            if response == "house mouse":
                speak("Perfect!")
                self.progress.emit("Perfect")
                self.countResponse()
                break
        
        self.progress.emit("SET B: \nSet - Net.")
        speak("Try this one.")
        
        while True:
            response = ask_ettibot().lower()
            if response == "set net":
                speak("Great!")
                self.progress.emit("Great!")
                self.countResponse()
                break
        
        self.progress.emit("SET C: \nBig - Small.")
        speak("How about this one?")
        
        while True:
            response = ask_ettibot().lower()   
            if response == "big small":
                speak("Well done!")
                self.progress.emit("Well done!")
                break
            
        self.finished.emit()
        
    def subjectNow2(self):
        subject = "Sentences and Non Sentences"
        #speaks(self.script)
        #speaks("Try to read the sets of words below")
        self.updateScreen("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
        speak("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
     
        self.updateScreen("Sentence\n\nA sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate. It begins with a capital letter and ends with a period ( . ), a question mark ( ? ), or an exclamation point ( ! ).")
        speak("A sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate.")
        speak("It begins with a capital letter and ends with a period, a question mark, or an exclamation point.")
        
        self.updateScreen("1. Ella plays the piano.\n2. The sun rises in the east.\n3. The garden is beautiful.")
        speak("Study the sample sentences below.")
        speak("Ella plays the piano.")
        speak("The sun rises in the east.")
        speak("The garden is beautiful.")
        
        self.updateScreen("Non-Sentences\n\nA non-sentence, like a phrase, is also a group of words. Unlike a sentence, it does not tell a complete thought or idea. It may just be the subject or the predicate.")
        speak("A non-sentence, like a phrase, is also a group of words.")
        speak("Unlike a sentence, it does not tell a complete thought or idea.")
        speak("It may just be the subject or the predicate.")
        
        self.updateScreen("1. playing the piano\n2. wide garden\n3. Ray and May")
        speak("Study the sample non-sentences below.")
        speak("playing the piano")
        speak("wide garden")
        speak("Ray and May")
        speak("Unlike a sentence, the examples below do not give complete thoughts or meanings.")
        
        speak("That's all for today's video, thank you for listening!")
        self.close()


class Subject(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/subject.ui', self)
        self.btnStart.clicked.connect(self.run)
        self.btnMenu.clicked.connect(self.showMenu)
        #self.showMaximized()  # opening window in maximized size
        
    def speak(self, text, lang="en"):  # here audio is var which contain text
        # Call LED lights here
        speaking = True
        tts = gTTS(text=text, lang=lang)
        filename = 'temp.mp3'
        tts.save(filename)
        playsound(filename, True)
        #pygame.mixer.music.load(filename)
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
          #  print("busy")
        
        #self.subjectLesson()
    def run(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        
        global flag
        flag = "Subject"
        #self.t1 = threading.Thread(name = "TranslateLoop", target=self.subjectNow)
        #self.t1.setDaemon(True)
        #self.t1.start()
        #MainThrd.stop()
        subjectLesson = "Rhyme"
        
        if subjectLesson == "Rhyme":
            #self.subjectNow()
            self.thread.started.connect(self.worker.subjectNow)
            self.subject_Title.setText(subjectLesson)
        
        if subjectLesson == "Express":
            #self.subjectNow2()
            self.thread.started.connect(self.worker.subjectNow2)
            self.subject_Title.setText(subjectLesson)
            
        if subjectLesson == "Sentence":
            #self.subjectNow3()
            self.thread.started.connect(self.worker.subjectNow3)
            
        if subjectLesson == "Stories":
            #self.subjectNow4()
            self.thread.started.connect(self.worker.subjectNow4)
        
        # Step 5: Connect signals and slots
        #self.thread.started.connect(self.worker.subjectNow)
        
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateScreen)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.btnStart.hide()
        self.btnStart.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.btnStart.setEnabled(True)
        )
        
        self.thread.finished.connect(
            lambda: self.btnStart.show()
        )
        
        self.thread.finished.connect(
            lambda: self.subtitle_2.setText("Click Start to Continue...")
        )
        
        
    def updateScreen(self, message):
        self.subtitle_2.setText(message)
        #self.subject_Title.setText(subject)
            
    def countResponse (self):
        global score
        score =+ 1
            
    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")
    
    def showMenu(self):
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Topics"
        #self.MainThrd.join()
        speak("topics")
        self.lesson = topics()
        self.lesson.show()
        #self.hide()
        self.close()
        #self.my_loop("topics")
        #MainThrd.join()
        MainMenu=False
        
        
        #window = MainMenu()
        #lesson.show()
        #threadSubj.stop()
        #MainThrd.start()
        #self.hide()
        
        
app = QApplication(sys.argv)
win = Subject()
win.show()
sys.exit(app.exec())