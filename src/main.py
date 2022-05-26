#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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

global activeScreen, speaking, duration, flag, subjectLesson, user_input, score, learner_name
learner_name = ""
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
energyThres = 70


################################################################################### GLOBAL FUNCTIONS #####################################################################

# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    print("Speak Now . . .")
    r.energy_threshold = energyThres
    r.dynamic_energy_threshold = False
    speaking=False
    
    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)  # phrase_time_limit=3)
        # Call LED lights here
        ard.ledListening()
        try:
            # Call LED lights here
            print("Recognising....")
            text = r.recognize_google(audio, language='en')
            print(text) 

        except Exception as e:
            print("ask etti: Exception " + str(e))
            return "0x01"

    return text

# function to convert the seconds into readable format
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600

    mins = seconds // 60
    seconds %= 60

    return hours, mins, seconds

# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    # Call LED lights here
    ard.ledSpeaking()
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
            
############################################################################################ SCREENS ###################################################################
    
############ SUBJECT1: RHYMING WORDS
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    
    def subjectNow(self):
        #speaks(self.script)
        #self.updateScreen(subject)
        #speaks("Try to read the sets of words below")
        self.progress.emit("In this lesson, you will learn about Rhyming Words.")
        speak("In this lesson, you will learn about Rhyming Words.")
        self.finished.emit()
        self.progress.emit("Words are formed by combining the letters of the alphabet.")
        speak("Words are formed by combining the letters of the alphabet.")
        self.progress.emit("It is important to remember that the English alphabet is composed of 26 letters with 5 vowels and 21 consonants.")
        speak("It is important to remember that the English alphabet is composed of 26 letters, with 5 vowels and 21 consonants.")
        self.progress.emit("Vowels: Aa  Ee Ii Oo Uu")
        speak("vowels are like, ah. ae. ē. oh. oooh.")
        self.progress.emit("Consonants: Bb Cc Dd Ff Gg Hh Jj Kk Ll Mm Nn Pp Qq Rr Ss Tt Vv Ww Xx Yy Zz.")
        speak("Now, consonants are like alphabets without vowels. Such as b,c,d,f,g, and so on.")
        self.progress.emit("By combining some of these letters, words may be formed.")
        speak("By combining some of these letters, words may be formed.")
        self.progress.emit("Some of these words include net, one, pen, and red. Some words have the same or similar ending sounds.")
        speak("Some of these words include net, one, pen, and red.Some words have the same or similar ending sounds.")
        self.progress.emit("They are called rhyming words. At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        speak("They are called rhyming words.At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        
        speak("Try to read the example below.")
        self.progress.emit("SET A: \nHouse - Mouse.")
        
        while True:
            response = ask_ettibot().lower()     
            if response == "house mouse":
                speak("Perfect!")
                self.progress.emit("Perfect")
                #self.countResponse()
                break
        
        self.progress.emit("SET B: \nSet - Net.")
        speak("Try this one.")
        
        while True:
            response = ask_ettibot().lower()
            if response == "set net":
                speak("Great!")
                self.progress.emit("Great!")
                #self.countResponse()
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
        
            
    def countResponse (self):
        global score
        score =+ 1
            
    def countClicks(self):
        self.clicksCount += 1
        #self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")
        
        
    # function to convert the seconds into readable format
    def convert(seconds):
        hours = seconds // 3600
        seconds %= 3600

        mins = seconds // 60
        seconds %= 60

        return hours, mins, seconds

    # HERE CONVERTS TEXT INTO VOICE OUTPUT
    def speak(self,text, lang="en"):  # here audio is var which contain text
        # Call LED lights here
        ard.ledSpeaking()
        speaking = True
        tts = gTTS(text=text)
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
        
            
    def stopThread (self):
        self.finished.emit()
        
############ SUBJECT2: SENTENCES AND NON-SENTENCES
class Worker2(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
        
    def subjectNow2(self):
        subject = "Sentences and Non Sentences"
        #speaks(self.script)
        #speaks("Try to read the sets of words below")
        self.progress.emit("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
        speak("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
     
        self.progress.emit("Sentence\n\nA sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate. It begins with a capital letter and ends with a period ( . ), a question mark ( ? ), or an exclamation point ( ! ).")
        speak("A sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate.")
        speak("It begins with a capital letter and ends with a period, a question mark, or an exclamation point.")
        
        self.progress.emit("1. Ella plays the piano.\n2. The sun rises in the east.\n3. The garden is beautiful.")
        speak("Study the sample sentences below.")
        speak("1. Ella plays the piano.")
        speak("Ella is the subject, while plays the piano is the predicate.")
        speak("2. The sun rises in the east.")
        speak("The sun is the subject, and rises in the east is the predicate.")
        speak("3. The garden is beautiful.")
        speak("The garden is the subject, and is beautiful is the predicate.")
        
        speak("Now.")
        
        self.progress.emit("Non-Sentences\n\nA non-sentence, like a phrase, is also a group of words. Unlike a sentence, it does not tell a complete thought or idea. It may just be the subject or the predicate.")
        speak("A non-sentence, like a phrase, is also a group of words.")
        speak("Unlike a sentence, it does not tell a complete thought or idea.")
        speak("It may just be the subject or the predicate.")
        
        self.progress.emit("1. playing the piano\n2. wide garden\n3. Ray and May")
        speak("Study the sample non-sentences below.")
        speak("1. playing the piano")
        speak("2. wide garden")
        speak("3. Ray and May")
        speak("Unlike a sentence, the examples below do not give complete thoughts or meanings.")
        speak("That's all for today's video, thank you for listening!")
        self.finished.emit()
            
    def countResponse (self):
        global score
        score =+ 1
            
    def countClicks(self):
        self.clicksCount += 1
        #self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")
        

############ SUBJECT3: Short Stories or Poems
class Worker3(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
        
    def subjectNow3(self):
        
        def emitStory():
            self.progress.emit("The New Toys")
            speak("The New Toys")
            
            self.progress.emit("Jay and Joy have new toys. \n Jay has a new toy car. It is small but shiny.\n Meanwhile, Joy has a new doll. It is big and beautiful.\n She hid them behind the table to surprise them.\n They hurriedly looked for the hidden gifts.\n When they saw them, they immediately opened them.\n They jumped for joy when they saw their new toys. They were just what they wished for.\n They thanked and kissed their Tita. They love their new toys.") 
            speak("Jay and Joy have new toys.")
            speak("Jay has a new toy car. It is small but shiny.")
            speak("Meanwhile,Joy has a new doll. It is big and beautiful.")
            speak("She hid them behind the table to surprise them.")
            speak("They hurriedly looked for the hidden gifts.") 
            speak("When they saw them, they immediately opened them.")
            speak("They jumped for joy when they saw their new toys. They were just what they wished for.")
            speak("They thanked and kissed their Tita. They love their new toys.")
            
        subject = "Details in Short Stories or Poems"
        #speaks(self.script)
        #speaks("Try to read the sets of words below")
        self.progress.emit("Are you familiar with short stories and poems?")
        speak("Are you familiar with short stories and poems?")
        
        self.progress.emit("You've possibly read and listened to different stories and poems")
        speak("You've possibly read and listened to different stories and poems,")
        
        self.progress.emit("such as fairy tales and other bedtime stories.")
        speak("such as fairy tales and other bedtime stories.")
        
        self.progress.emit("These stories and poems tell us what the characters feel and do. They may also teach us important lessons in life.")
        speak("These stories and poems tell us what the characters feel and do. They may also teach us important lessons in life.")
        
        self.progress.emit("Now. Listen to this story.")
        speak("Now. Listen to this story,")
        
        emitStory()
        
        speak("Try to answer these questions")
        self.progress.emit("Who received gifts during their birthday?")
        speak("Who received gifts during their birthday?")
    
        while True:
            response = ask_ettibot().lower()     
            if any(i in response for i in ["jay", "joy", "jay and joy", "j n joy"]):
                speak("Perfect!")
                ard.nod()
                self.progress.emit("jay and joy")
                sleep(3)
                self.countResponse()
                break
            
            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                continue
            
            else:
                res = np.random.choice(
                    ["Nope, Try again.", "incorrect", "I heard you, but I think it's not right", "uh nope, try again"])
                speak(res)
                ard.notNod()
                
        self.progress.emit("Who gave them the gifts?")
        speak("Who gave them the gifts?")
        while True:
            response = ask_ettibot().lower()     
            if any(i in response for i in ["tita", "auntie"]):
                speak("Perfect!")
                self.progress.emit("tita")
                ard.nod()
                sleep(3)
                self.countResponse()
                break
            
            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                continue
            
            else:
                res = np.random.choice(
                    ["Nope, Try again.", "incorrect", "I heard you, but I think it's not right", "uh nope, try again"])
                speak(res)
                ard.notNod()
                
        self.progress.emit("Where did she hide the gifts?")
        speak("Where did she hide the gifts?")
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["table", "behind the table"]):
                speak("Great!")
                self.progress.emit("behind the table")
                ard.nod()
                sleep(3)
                self.countResponse()
                break
            
            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                continue
            
            else:
                res = np.random.choice(
                    ["Nope, Try again.", "incorrect", "I heard you, but I think it's not right", "uh nope, try again"])
                speak(res)
                ard.notNod()
                
        self.progress.emit("What gifts did they receive?")
        speak("What gifts did they receive?")
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["toy car and doll", "car", "doll", "toy"]):
                speak("Perfect!")
                self.progress.emit("toy car and doll")
                ard.nod()
                sleep(3)
                self.countResponse()
                break
            
            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                continue
            
            else:
                res = np.random.choice(
                    ["Nope, Try again.", "incorrect", "I heard you, but I think it's not right", "uh nope, try again"])
                speak(res)
                ard.notNod()
                
        self.progress.emit("What did they do when they found the gifts?")
        speak("What did they do when they found the gifts?")
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["jumped", "jump", "jumped for joy"]):
                speak("Well done!")
                self.progress.emit("they jumped for joy")
                ard.nod()
                sleep(3)
                self.countResponse()
                break
            
            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                continue
            
            else:
                res = np.random.choice(
                    ["Nope, Try again.", "incorrect", "I heard you, but I think it's not right", "uh nope, try again"])
                speak(res)
                ard.notNod()
                
                
        speak("That's all for today's video, thank you for listening!")
        self.finished.emit()
            
    def countResponse (self):
        global score
        score =+ 1
            
    def countClicks(self):
        self.clicksCount += 1
        #self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")
        

############ SUBJECT4: Polite Expressions
class Worker4(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    image = pyqtSignal()
        
    def subjectNow4(self):
        subject = "Polite Expressions"
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        self.progress.emit("Politeness is one of the characteristics that you should have.")
        speak("Politeness is one of the characteristics that you should have.")
        
        self.progress.emit("There are lots of ways on how one can show politeness.")
        speak("There are lots of ways on how one can show politeness.")
        
        self.progress.emit("Saying po and opo is one of these ways")
        speak("Saying")
        speak("po at opo", "tl")
        speak("is one of these ways.")
        
        self.progress.emit("Also, you can show politeness using appropriate words or expressions in different events.")
        speak("Also, you can show politeness using appropriate words or expressions in different events.")
    
        self.progress.emit("At the end of the lesson, you are expected to use respond appropriately to polite expressions in greetings, leave takings, expressing gratitude and apology, asking permission, and offering help. ")
        speak("At the end of the lesson, you are expected to use respond appropriately to polite expressions in greetings leave takings, expressing gratitude and apology, asking permission, and offering help.")
        
        self.progress.emit("Read the example shown on screen. ")
        speak("Read the example shown on screen. ")
        
        self.progress.emit("\n")
        self.image.emit()
        
        sleep(7)
        
        speak("Notice the highlighted words.")
        speak("Good afternoon, Thank you very much. and You are welcome are examples of polite greetings. that you may use in talking to other people. ")
        
        
        self.progress.emit("That's All, Thank you for listening!")
        speak("That's all for today's discussion, thank you for listening!")
        
        sleep(3)
        self.finished.emit()
            
    def countResponse (self):
        global score
        score =+ 1
            
    def countClicks(self):
        self.clicksCount += 1
        #self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")


########################################################################### DYNAMIC SCREEN SUBJECT #########################################################
class Subject(QWidget):  # second screen showing the discussion screen
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/subject.ui', self)
        self.btnStart.clicked.connect(self.run)
        self.btnMenu.clicked.connect(self.showMenu)
        self.showMaximized()  # opening window in maximized size
        #self.updateImage()
        
        
    def updateImage(self, url='images/polite expression.png'):
        pixmap = QPixmap(url)
        self.subtitle_2.setPixmap(pixmap)
        self.subtitle_2.setScaledContents(True)
        #self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())
        
        #document = self.subtitle_2.document()
        #self.resize(1024, 600)
        #cursor = QTextCursor(document)
        #p1 = cursor.position() # returns int
        #cursor.insertImage(url)
        
        
    def updateScreen(self, message):
        self.subtitle_2.setText(message)
        self.subtitle_2.setAlignment(Qt.AlignCenter)
        #self.subject_Title.setText(subject)
        
    def speak(self, text, lang="en"):  # here audio is var which contain text
        # Call LED lights here
        ard.ledSpeaking()
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
          
    def showMenu(self):
        # Step 2: Create a QThread object
        #self.thread = QThread()
        # Step 3: Create a worker object
        worker = Worker()
        # Step 4: Move worker to the thread
        worker.stopThread()
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Topics"
        #self.MainThrd.join()
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
        
    def run(self):
        global flag, subjectLesson
        flag = "Subject"
        #self.t1 = threading.Thread(name = "TranslateLoop", target=self.subjectNow)
        #self.t1.setDaemon(True)
        #self.t1.start()
        #MainThrd.stop()
        
        if subjectLesson == "Rhyming Words":
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            #self.subjectNow()
            self.thread.started.connect(self.worker.subjectNow)
            self.subject_Title.setText(subjectLesson)
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateScreen)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.btnStart.hide()
            self.btnMenu.hide()
            self.btnStart.setEnabled(False)
            
            self.thread.finished.connect(
                lambda: self.btnStart.setEnabled(True)
            )
            
            self.thread.finished.connect(
                lambda: self.btnStart.show()
            )
            
            self.thread.finished.connect(
                lambda: self.btnMenu.show()
            )
            
            self.thread.finished.connect(
                lambda: self.subtitle_2.setText("Click Start to Continue...")
            )
            
            self.thread.finished.connect(
                lambda: self.showMenu()
            )
            
        if subjectLesson == "Sentence":
            
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker2()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            #self.subjectNow()
            self.thread.started.connect(self.worker.subjectNow2)
            self.subject_Title.setText("Sentences and Non-Sentences")
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateScreen)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.btnStart.hide()
            self.btnMenu.hide()
            self.btnStart.setEnabled(False)
            
            self.thread.finished.connect(
                lambda: self.btnStart.setEnabled(True)
            )
            
            self.thread.finished.connect(
                lambda: self.btnStart.show()
            )
            
            self.thread.finished.connect(
                lambda: self.btnMenu.show()
            )
            
            self.thread.finished.connect(
                lambda: self.subtitle_2.setText("Click Start to Continue...")
            )
            
            self.thread.finished.connect(
                lambda: self.showMenu()
            )
        
        if subjectLesson == "Stories":
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker3()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            #self.subjectNow()
            self.thread.started.connect(self.worker.subjectNow3)
            self.subject_Title.setText("Sentences and Non-Sentences")
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateScreen)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.btnStart.hide()
            self.btnMenu.hide()
            self.btnStart.setEnabled(False)
            
            self.thread.finished.connect(
                lambda: self.btnStart.setEnabled(True)
            )
            
            self.thread.finished.connect(
                lambda: self.btnStart.show()
            )
            
            self.thread.finished.connect(
                lambda: self.btnMenu.show()
            )
            
            self.thread.finished.connect(
                lambda: self.subtitle_2.setText("Click Start to Continue...")
            )
            
            self.thread.finished.connect(
                lambda: self.showMenu()
            )

        
        if subjectLesson == "Express":
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker4()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            #self.subjectNow()
            self.thread.started.connect(self.worker.subjectNow4)
            self.subject_Title.setText("Polite Expressions")
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.image.connect(self.updateImage)
            self.worker.progress.connect(self.updateScreen)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.btnStart.hide()
            self.btnMenu.hide()
            self.btnStart.setEnabled(False)
            
            self.thread.finished.connect(
                lambda: self.btnStart.setEnabled(True)
            )
            
            self.thread.finished.connect(
                lambda: self.btnStart.show()
            )
            
            self.thread.finished.connect(
                lambda: self.btnMenu.show()
            )
            
            self.thread.finished.connect(
                lambda: self.subtitle_2.setText("Click Start to Continue...")
            )
            
            self.thread.finished.connect(
                lambda: self.showMenu()
            )
        
  
########################################################################### TOPICS Screen  #####################################################################
class topics(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/topics.ui', self)
        self.showMaximized()  # opening window in maximized size
        activeScreen = "topics"
        #sleep(duration)
        self.btnMenu.clicked.connect(self.showMenu)
        
        self.btnExpress.clicked.connect(self.showExpress)
        self.btnRhyming.clicked.connect(self.showRhyme)
        self.btnSentence.clicked.connect(self.showSentence)
        self.btnStories.clicked.connect(self.showStories)
        self.btnStart.clicked.connect(self.startLesson)
            
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)
        
    def startLesson(self):
        self.showRhyme()
        
    def run(self):
        global flag
        flag = "Topics"
        #initialize audio for listening in background
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = energyThres
            
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)
        
        
    def showRhyme(self):
        global subjectLesson
        subjectLesson = self.btnRhyming.text()
        speak(self.btnRhyming.text())
        #self.threadTopic.stop()
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()
        
        
    def showExpress(self):
        global subjectLesson
        subjectLesson = "Express"
        self.Topics.setText(self.btnExpress.text())
        speak(self.btnExpress.text())
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()
        
        
    def showSentence(self):
        global subjectLesson
        subjectLesson = "Sentence"
        self.Topics.setText(self.btnSentence.text())
        speak(self.btnSentence.text())
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()
        
    def showStories(self):
        global subjectLesson
        subjectLesson = "Stories"
        self.Topics.setText(self.btnStories.text())
        speak(self.btnStories.text())
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()
        
    def showMenu(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Topics"
        window = MainMenu()
        window.show()
        speak("Main Menu")
        #self.hide()
        self.close()
        
    def updateScreen(self, text):    
        self.Topics.setText(text)
        
        
    # this is called from the background thread
    def callback(self, recognizer, audio):
        ard.ledListening()
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + text)
            self.recognizedWords(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            
    def recognizedWords(self, text):
        global user_input, flag
        user_input = text
        print (text)
        
        if flag == "Topics":
            query = text
            #print("Speaking: "+str(speaking))
            #window = MainMenu ()
            self.updateScreen(f"You: {query}")
            #print(query)
            #if window.isVisible():
            #    print("Main Menu is Visible")
                
            #elif splash.isVisible():
            #    print("Splash is Visible")
            
            # rhyme
            if any(i in query for i in ["rhyme", "rhyming word", "show rhyme", "rhyming words"]):
                self.showRhyme()
                self.stop_listening(wait_for_stop=False)

            # sentence
            elif any(i in query for i in ["sentence", "sentences"]):
                self.showSentence()
                self.stop_listening(wait_for_stop=False)
                
            # express
            elif any(i in query for i in ["express", "polite expression"]):
                self.showExpress()
                self.stop_listening(wait_for_stop=False)
                
            # stories
            elif any(i in query for i in ["story", "stories"]):
                self.showStories()
                self.stop_listening(wait_for_stop=False)
                
            #menu
            elif any(i in query for i in ["menu", "main menu"]):
                self.showMenu()
                self.stop_listening(wait_for_stop=False)
                
            
            
            # respond politely
            elif any(_ in query for _ in ["thank", "thanks"]):
                res = np.random.choice(
                    ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
                speak(res)

                
            # respond politely
            elif any(_ in query for _ in ["good morning", "morning"]):
                res = np.random.choice(
                    ["Good morning human", "good morning too!"])
                speak(res)
                

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                
                speak(res)
                self.updateScreen(f"Etti: {res}")
                ard.nod()
                
            elif "none" in query:
                print(query)
                
            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you.", "Sorry?"])
                speak(res)
                print(query)
    

########################################################################################  TRANSLATE Screen  #######################################################             
class TranslateWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    
    def run(self):
        speak("You can translate English words to Filipino and vise versa. Just speak the word you want to translate. Then the output would be the opposite language.")
        self.finished.emit()

        
class TranslatorScreen(QDialog): 
    def __init__(self):
        super().__init__()
        uic.loadUi('Translator.ui', self)
        activeScreen = "Translator"
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnHow.clicked.connect(self.showHow)
        self.showMaximized()  # opening window in maximized size
        #self.start_button()
        #checkPlaying()
        #checkPlaying()
        #speak("at sasabihin ko sa wikang filipino ay. Magandang Umaga!", "tl")
        #self.t1 = threading.Thread(name = "TranslateLoop", target=self.translateNow)
        #self.t1.setDaemon(True)
        
        #initialize audio for listening in background
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(self.m, self.callback)

        
    def updateScreen(self, inputTxt="User Input", outputTxt="Translation"):
        self.transInput.setText(f"You: {inputTxt}")
        self.transOutput.setText(outputTxt)
        
    def showHow(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = TranslateWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        #self.subjectNow()
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateScreen)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.btnHow.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.btnHow.setEnabled(True)
        )
        
        
    def showMenu(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "MainMenu"
        self.window = MainMenu()
        #Thread 1
        #MyLoop = threading.Thread(name="MenuLoop", target=window.my_loop)
        #MyLoop.setDaemon(True)
        #MyLoop.start()
        self.window.show()
        self.close()
        
        
    def run(self):
        global flag
        flag = "Translate"
        
        #initialize audio for listening in background
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)
        #self.t1.start()
        
        
    # this is called from the background thread
    def callback(self, recognizer, audio):
        ard.ledListening()
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + text)
            self.recognizedWords(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            
    def recognizedWords(self, text):
        global user_input, flag
        user_input = text
        print (text)
        
        #if flag == "Translate":
        query = text
        #print("Speaking: "+str(speaking))
        #window = MainMenu ()
        self.updateScreen(f"You: {query}")
        word = text
        prefix = 'translate'
        print(word[word.startswith(prefix) and len(prefix):])
        stippedWord = word[word.startswith(prefix) and len(prefix):]
        #translatr.updateScreen(word)
        #print(f"User Input: {word}")
        detected_lang = translator.detect(word)
        
        if detected_lang.lang == 'en':
            translate_text = translator.translate(stippedWord, dest='tl')
            print(f"Translation: {translate_text.text}")
            output = translate_text.text
            self.updateScreen(stippedWord, output)
            speak(translate_text.text, 'tl')

        elif detected_lang.lang == 'tl':
            translate_text = translator.translate(stippedWord, dest='en')
            print(f"Translation: {translate_text.text}")
            output = translate_text.text
            self.updateScreen(stippedWord, output)
            speak(translate_text.text, 'en')
                    
        
        # respond politely
        elif any(_ in query for _ in ["thank", "thanks"]):
            res = np.random.choice(
                ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
            speak(res)

        # respond politely
        elif any(i in query for i in ["hi", "hello", "can you hear me"]):
            res = np.random.choice(
                ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
            speak(res)
                      
        elif "menu" in query:
            self.showMenu()
            
        elif "none" in query:
            print(query)
            

        else:
            res = np.random.choice(
                ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you."])
            speak(res)
            print(query)
        
        
    def translateNow(self):
        #Translate: the bot will get user input then recognize if the input is english or tagalog
        #then bot will convert the input into opposite language and speak the output
        speak("You can try saying. Translate, then the word you want to translate. For example, translate Goodmorning")
        while flag == "Translate":
            
            if flag != "Translate":
                print("flag is not Translate")
                break
            
            print("Flag: " +flag)
            query = ask_ettibot().lower()  
            word = query
            prefix = 'translate'
            print(word[word.startswith(prefix) and len(prefix):])
            stippedWord = word[word.startswith(prefix) and len(prefix):]
            #translatr.updateScreen(word)
            #print(f"User Input: {word}")
            detected_lang = translator.detect(word)
            if any(i in query for i in ["translate", "salin wika", "translation"]):
                try: 
                    if detected_lang.lang == 'en':
                        translate_text = translator.translate(stippedWord, dest='tl')
                        print(f"Translation: {translate_text.text}")
                        output = translate_text.text
                        self.updateScreen(stippedWord, output)
                        speak(translate_text.text, 'tl')
                        
                        

                    elif detected_lang.lang == 'tl':
                        translate_text = translator.translate(stippedWord, dest='en')
                        print(f"Translation: {translate_text.text}")
                        output = translate_text.text
                        self.updateScreen(stippedWord, output)
                        speak(translate_text.text, 'en')
                        
                        
                        
                except Exception as e:
                    print("Translate Exception " + str(e))
                    #speak("You can try saying translate and the word you want to translate. For example, translate goodmorning")
                    continue
            
            # respond politely
            elif any(_ in query for _ in ["thank", "thanks"]):
                res = np.random.choice(
                    ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
                speak(res)

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                speak(res)
                          
            elif "menu" in query:
                self.showMenu()
                
            elif "none" in query:
                print(query)
                

            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you."])
                speak(res)
                print(query)
                
            #else:
            #    continue
                

######################################################################## QUIZ SCREEN ###################################################################################
############ SUBJECT1: RHYMING WORDS
class QuizWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str, bool)
    button = pyqtSignal(str,str)
    
    def Quiz1(self):
        
        global user_input, score
        
        self.button.emit("NO", "YES")
        self.progress.emit("Identify whether the words shown are rhyming or not rhyming. Answer by clicking the button or with your voice saying the word 'YES' if it's rhyming and 'NO' if it's not rhyming words.\n", True)
        speak("Identify whether the words shown are rhyming or not rhyming. You can answer by clicking the buttons or with your voice saying the word yes if it's rhyming and no if it's not.")
        
        speak("ready?")
        
        def q1():
            self.progress.emit("1. Car - bar", True)
            speak("number 1. car. bar")
            
        def q2():
            self.progress.emit("2. sail - tail", True)
            speak("number 2. sail. tail")
            
        def q3():
            self.progress.emit("3. can - cat", True)
            speak("number 3. can. cat")
            
        def q4():
            self.progress.emit("4. pig - wig", True)
            speak("number 4. pig. wig")
            
        def q5():
            self.progress.emit("5. map - hut", True)
            speak("number 5. map. hut")
            
        q1()    
        while True:
            response = user_input   
            if any(_ in response for _ in ["yes", "rhyming"]) or user_input == "yes":
                speak("Perfect!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["no", "not"]) or user_input == "no":
                speak("uhm")
                break
            
        user_input = ""
   
        q2()  
        while True:
            response = user_input
            if any(_ in response for _ in ["yes", "rhyming"]) or user_input == "yes":
                speak("Great!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["no", "not"]) or user_input == "no":
                speak("uh oh!")
                break
        
        user_input = ""
   
        q3()  
        while True:
            response = user_input
            if any(_ in response for _ in ["no", "not"]) or user_input == "no":
                speak("Great!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["yes", "rhyming"]) or user_input == "yes":
                speak("nope!")
                break
            
        user_input = ""
   
        q4()  
        while True:
            response = user_input
            if any(_ in response for _ in ["yes", "rhyming"]) or user_input == "yes":
                speak("Great!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["no", "not"]) or user_input == "no":
                speak("nice try!")
                break
            
        user_input = ""
   
        q5()  
        while True:
            response = user_input
            if any(_ in response for _ in ["no", "not"]) or user_input == "no":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["yes", "rhyming"]) or user_input == "yes":
                speak("nope!")
                break
            
        user_input = ""
        
        self.progress.emit(f"You've got {score} out of 5.", False)
        speak(f"You've got {score} out of 5.")
        
        if score >= 3:
            self.progress.emit("You did well! :)", True)
            speak("You did well, uwu!")
            
            
        elif score < 3:
            self.progress.emit("Try again Next Time :(", True)
            speak("Try again Next Time")
        
        
        self.finished.emit()
        score = 0
        
        
############ SUBJECT1: SENTENCES AND NON SENTENCES
class QuizWorker2(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str, bool)
    button = pyqtSignal(str,str)
    
    #Sentences and NSn sentences
    def Quiz2(self):
        
        global user_input, score
        
        self.button.emit("S", "NS")
        self.progress.emit("Say S if the given item is a sentence and NS if it is a Non-sentence.\n", True)
        speak("Say S. if the given item is a sentence. and NS. if it is a Non-sentence.")
        
        speak("ready?")
        
        def q1():
            self.progress.emit("1. My name is Paula Marie.", True)
            speak("number 1. My name is Paula Marie.")
            
        def q2():
            self.progress.emit("2. my wonderful pet", True)
            speak("number 2. my wonderful pet")
            
        def q3():
            self.progress.emit("3. Anna’s new phone", True)
            speak("number 3. Anna’s new phone")
            
        def q4():
            self.progress.emit("4. What is your name?", True)
            speak("number 4. What is your name?")
            
        def q5():
            self.progress.emit("5. her father’s house", True)
            speak("number 5. her father’s house")
            
        def q6():
            self.progress.emit("6. The children are playing.", True)
            speak("number 6. The children are playing.")
            
        def q7():
            self.progress.emit("7. Ramon sings a song.", True)
            speak("number 7. Ramon sings a song.")

        def q8():
            self.progress.emit("8. I am sorry.", True)
            speak("number 8. I am sorry.")

        def q9():
            self.progress.emit("9. playing the piano", True)
            speak("number 9. playing the piano")

        def q10():
            self.progress.emit("10. Selling some apples", True)
            speak("number 10. selling some apples")
            
        q1()    
        while True:
            response = user_input   
            if any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Perfect!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("uhm")
                break
            
        user_input = ""
   
        q2()  
        while True:
            response = user_input
            if any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("Great!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("uh oh!")
                break
        
        user_input = ""
   
        q3()  
        while True:
            response = user_input
            if any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Great!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("Nope!")
                break
            
        user_input = ""
   
        q4()  
        while True:
            response = user_input
            if any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Great!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("nice try!")
                break
            
        user_input = ""
   
        q5()  
        while True:
            response = user_input
            if any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Nope!")
                break
       
        user_input = ""
                   
        q6()  
        while True:
            response = user_input
            if any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("nice try!")
                break
            
        user_input = ""
                   
        q7()  
        while True:
            response = user_input
            if any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("Nope!")
                break
            
        user_input = ""
                   
                   
        q8()  
        while True:
            response = user_input
            if any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("Nope!")
                break
            
        user_input = ""
                   
       
        q9()  
        while True:
            response = user_input
            if any(_ in response for _ in ["NS"]) or user_input == "NS":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("nice try!")
                break
            
        user_input = ""
                   
                   
        q10()  
        while True:
            response = user_input
            if any(_ in response for _ in ["NS", "ns"]) or user_input == "NS":
                speak("Well Done!")
                #self.countResponse()
                score += 1
                break
            
            elif any(_ in response for _ in ["S", "s"]) or user_input == "S":
                speak("nice try!")
                break
            
        user_input = ""            
                   
        
        self.progress.emit(f"You've got {score} out of 10.", False)
        speak(f"You've got {score} out of 10.")
        
        if score >= 5:
            self.progress.emit("You did well! :)", True)
            speak("You did well!")
            
            
        elif score < 5:
            self.progress.emit("Try again Next Time :(", True)
            speak("Try again Next Time")
        
        
        self.finished.emit()
        score = 0


        
        
class QuizMain(QWidget):  # second screen showing the quiz screen
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Q1.ui', self)
        self.btnFalse.clicked.connect(self.falseButton)
        self.btnTrue.clicked.connect(self.trueButton)
        self.showMaximized()  # opening window in maximized size
        
        
    def run(self):
        global flag, subjectLesson
        flag = "Quiz"

        if subjectLesson == "Rhyming and Non-Rhyming":
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = QuizWorker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            #self.subjectNow()
            self.thread.started.connect(self.worker.Quiz1)
            self.quiz_Title.setText(subjectLesson)
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateScreen)
            self.worker.button.connect(self.updateButton)
            
            # Step 6: Start the thread
            self.thread.start()

            # Final reset
            self.thread.finished.connect(
                lambda: self.showMenu()
            )
            
        elif subjectLesson == "Sentence":
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = QuizWorker2()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            #self.subjectNow()
            self.thread.started.connect(self.worker.Quiz2)
            self.quiz_Title.setText(subjectLesson)
            
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateScreen)
            self.worker.button.connect(self.updateButton)
            
            # Step 6: Start the thread
            self.thread.start()

            # Final reset
            self.thread.finished.connect(
                lambda: self.showMenu()
            )
            
            
    def showMenu(self):
        worker = Worker()
        worker.stopThread()
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Quiz Screen"
        self.quiz = QuizScreen()
        self.quiz.show()
        #self.hide()
        self.close()
        #self.my_loop("topics")
       
        
            
    def updateButton (self, opt1, opt2):
        self.btnFalse.setText(opt1)
        self.btnTrue.setText(opt2)
    
    def updateScreen(self, message, append=True):
        if append:
            self.subtitle_2.append(message)
        
        elif not append:
            self.subtitle_2.setText(message)
        
        self.subtitle_2.setAlignment(Qt.AlignCenter)
        #self.subject_Title.setText(subject)
        
    def falseButton(self):
        btnFalse = self.btnFalse.text()
        global user_input
        user_input = btnFalse
        print("validate the answer if false")
        
    def trueButton(self):
        btnTrue = self.btnTrue.text()
        global user_input
        user_input = btnTrue
        print("validate the answer if true")
        
        
            
class QuizScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Quizzes.ui', self)
        self.showMaximized()  # opening window in maximized size
        self.btnStart.clicked.connect(self.showMenu)
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnExpress.clicked.connect(self.showExpress)
        self.btnRhyming.clicked.connect(self.showRhyme)
        self.btnSentence.clicked.connect(self.showSentence)
            
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)
        
        
    def showRhyme(self):
        global subjectLesson
        subjectLesson = self.btnRhyming.text()
        speak(self.btnRhyming.text())
        #self.threadTopic.stop()
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()
        
        
    def showExpress(self):
        global subjectLesson
        subjectLesson = "Express"
        speak(self.btnExpress.text())
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()
        
        
    def showSentence(self):
        global subjectLesson
        subjectLesson = "Sentence"
        speak(self.btnSentence.text())
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()
        
    def showStories(self):
        global subjectLesson
        subjectLesson = "Stories"
        #self.Topics.setText(self.btnStories.text())
        speak(self.btnStories.text())
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()
        
    def showMenu(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "MainMenu"
        window = MainMenu()
        speak("Main Menu")
        #Thread 1
        #MyLoop = threading.Thread(name="MenuLoop", target=window.my_loop)
        #MyLoop.setDaemon(True)
        #MyLoop.start()
        window.show()
        self.close()
        
    def updateScreen(self, text):    
        self.Title.setText(text)
    
    # this is called from the background thread
    def callback(self, recognizer, audio):
        ard.ledListening()
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + text)
            self.recognizedWords(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            
    def recognizedWords(self, text):
        global user_input, flag
        user_input = text
        print (text)
        
        if flag == "Quiz Screen":
            query = text
            #print("Speaking: "+str(speaking))
            #window = MainMenu ()
            self.updateScreen(f"You: {query}")
            #print(query)
            #if window.isVisible():
            #    print("Main Menu is Visible")
                
            #elif splash.isVisible():
            #    print("Splash is Visible")
            
            # topics
            if any(i in query for i in ["rhyme", "rhyming", "first"]):
                self.showRhyme()
                self.stop_listening(wait_for_stop=False)

            # quiz
            elif any(i in query for i in ["express", "second", "what's the challenge"]):
                self.showExpress()
                self.stop_listening(wait_for_stop=False)
                
    

            # respond politely
            elif any(_ in query for _ in ["thank", "thanks"]):
                res = np.random.choice(
                    ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
                speak(res)

                
            # respond politely
            elif any(_ in query for _ in ["good morning", "morning"]):
                res = np.random.choice(
                    ["Good morning human", "good morning too!"])
                speak(res)
                

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                
                speak(res)
                self.updateScreen(f"Etti: {res}")
                ard.nod()
                
            elif "none" in query:
                print(query)
                
            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you.", "Sorry?"])
                speak(res)
                print(query)


                

######################################################################## MAIN MENU SCREEN ###################################################################################        
class MenuWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    time = pyqtSignal()
    
    def run(self):
        ard.nod()
        speak("I'm Etti, I am programmed to teach basic english for my children and communicate with people, just like you!")
        ard.lookStraight()
        self.finished.emit()
        
    def updateTime(self):
        while True:
            self.time.emit()
            
    
              
              
class MainMenu(QWidget):
    def __init__(self):
        global flag
        flag = "MainMenu"
        threading.current_thread().name = "Menu"
        super().__init__()
        uic.loadUi('screens/welcome.ui', self) # MainWindow.ui
        self.showMaximized()  # opening window in maximized size
        #activeScreen = "MainMenu"
        # Create and connect widgets
        self.btnTopics.clicked.connect(self.runTopics)
        self.btnQuiz.clicked.connect(self.runQuiz)
        self.btnTranslate.clicked.connect(self.runTranslate)
        self.btnAbout.clicked.connect(self.runAbout)
        
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)

        
    def run():
        # Step 2: Create a QThread object
        thread = QThread()
        # Step 3: Create a worker object
        worker = MenuWorker()
        # Step 4: Move worker to the thread
        worker.moveToThread(self.thread)
        #self.subjectNow()
        thread.started.connect(self.worker.updateTime)
        worker.finished.connect(self.thread.quit)
        worker.finished.connect(self.worker.deleteLater)
        thread.finished.connect(self.thread.deleteLater)
        worker.time.connect(self.updateScreenTime)
        # Step 6: Start the thread
        thread.start()
        

        
    def runTopics(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Topics"
        #self.MainThrd.join()
        speak(self.btnTopics.text())
        self.lesson = topics()
        self.lesson.show()
        self.hide()
        #self.close()
        #self.my_loop("topics")
        #MainThrd.join()
        MainMenu=False
      
    def updateScreenTime(self):
        x = datetime.datetime.now()
        Day = x.strftime("%A")
        Month = x.strftime("%B")
        DayInt = x.strftime("%d")
        
        Hour = x.strftime("%I")
        Minute = x.strftime("%M")
        Seconds =  x.strftime("%S")
        Meridian =  x.strftime("%p")
        
        
        self.date.setText(f"{Month}, {Day}")
        self.day.setText(Day)
        self.time.setText(f"{Hour}:{Minute}:{Seconds} {Meridian}")
        
    def updateScreen(self, text):    
        self.Title.setText(text)
        
    def runQuiz(self):
        # self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Quiz Screen"
        speak(self.btnQuiz.text())
        #self.MainThrd.close()
        #speak("Quizzes")
        self.quiz = QuizScreen()
        self.quiz.show()
        #self.hide()
        self.close()
        
        
    def runTranslate(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Translate"
        #self.MainThrd.close()
        speak(self.btnTranslate.text())
        self.translate = TranslatorScreen()
        self.translate.show()
        self.translate.run()
        #self.hide()
        self.close()
        
        
    def runAbout(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = MenuWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateScreen)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.btnAbout.setEnabled(False)
        
        self.thread.finished.connect(
            lambda: self.btnAbout.setEnabled(True)
        )
        
    # this is called from the background thread
    def callback(self, recognizer, audio):
        ard.ledListening()
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + text)
            self.recognizedWords(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            
    def recognizedWords(self, text):
        global user_input, flag
        user_input = text
        print (text)
        
        if flag == "MainMenu":
            query = text
            #print("Speaking: "+str(speaking))
            #window = MainMenu ()
            self.updateScreen(f"You: {query}")
            #print(query)
            #if window.isVisible():
            #    print("Main Menu is Visible")
                
            #elif splash.isVisible():
            #    print("Splash is Visible")
            
            # topics
            if any(i in query for i in ["topic", "topics", "show topics", "what's the lessons"]):
                self.stop_listening(wait_for_stop=False)
                self.runTopics()
                self.close()

            # quiz
            elif any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
                self.stop_listening(wait_for_stop=False)
                flag = "Quiz"
                #self.MainThrd.close()
                #speak("Quizzes")
                quiz = QuizScreen()
                quiz.show()
                #self.hide()
                self.close()
                
            # translate
            elif flag == "Translate":
                print("flag is Translate")
               
            
            elif any(i in query for i in ["translate", "salin wika", "translation"]):
                self.runTranslate()
                
                self.hide()
                self.stop_listening(wait_for_stop=False)
            
            # about me
            elif "about" in query:
                self.runAbout() 


            # respond politely
            elif any(_ in query for _ in ["thank", "thanks"]):
                res = np.random.choice(
                    ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
                speak(res)

                
            # respond politely
            elif any(_ in query for _ in ["good morning", "morning"]):
                res = np.random.choice(
                    ["Good morning human", "good morning too!"])
                speak(res)
                ard.lookLeft()
                

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                
                speak(res)
                self.updateScreen(f"Etti: {res}")
                ard.nod()
                ard.lookStraight()
                
            elif any(i in query for i in ["up", "look up"]):
                ard.lookUp()
                
                
            elif any(i in query for i in ["down", "look down"]):
                ard.lookDown()
                
                
            elif any(i in query for i in ["left", "look left"]):
                ard.lookLeft()
                
            elif any(i in query for i in ["right", "look right"]):
                ard.lookRight()
                
                
            elif any(i in query for i in ["disagree", "disaffirm"]):
                ard.notNod()
                ard.lookStraight()
                
            elif any(i in query for i in ["agree", "affirm"]):
                ard.nod()
                ard.lookStraight()
                
                
            elif "none" in query:
                print(query)
                
            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you.", "Sorry?"])
                speak(res)
                print(query)
                
        
    def gotoMenu(self):
        self.show()
    
                
   
def myThread():
    speak("Good Day, learner!")
    ard.ledAll()
    
    while True:
        if flag == "Quiz":
            print(f"Score: {score}")
            
        print(f"Learner's Name: {learner_name}")
        print(f"User voice: {user_input}")
        print(f"Counter: {counter}")
        print(f"FLAG: {flag}")
        print(f"Subject: {subjectLesson}")
        print(threading.enumerate())
        time.sleep(1)
        try:
            pass
        
        except KeyboardInterrupt:
            sys.exit(0)
        
            
            
def main():
    app = QApplication(sys.argv)
    speak("ooohh woooh?")
    print("Mainthread: Started")
    #initialize audio for listening in background
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = energyThres
        
    window = MainMenu()
    #window.run()
    window.show()
    
    #MainThrd.join()
    
    #Enumerate Running Threads
    checkThread = threading.Thread(name="Enumerate", target=myThread)
    checkThread.setDaemon(True)
    checkThread.start()
    
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    #Main Thread
    main()
    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    