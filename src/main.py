#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#openAI
import openai

import logging
import random
import sys
import time

import os
import datetime
import numpy as np
import pygame
from pygame import mixer
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

from PyQt5 import QtGui
from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import *

# nltk ====
import nltk
from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.tokenize.treebank import TreebankWordDetokenizer

translator= Translator()
now = QDate.currentDate()


#pygame.mixer.pre_init(22050, 16, 1, 4096) #frequency, size, channels, buffersize
pygame.mixer.init()
pygame.init()
logging.basicConfig(format="%(message)s", level=logging.INFO)

openai.api_key = "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"
            
#####################################   GLOBAL CONTAINERS   ##############################
global activeScreen, speaking, duration, flag, subjectLesson, user_input, score, learner_name, timer, bot_response
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
speaking = False
flag = ""
energyThres = 302
timer = 0

thanked = ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"]
greet = ["hi", "hello!", "yes?", "hi there"]
greet2 = ["good morning", "good day"]
micTest = ["I can hear you", "loud and clear"]
praise = ["Perfect", "great!", "Well Done", "good job!", "nice!", "Excellent!"]
disagrees =  ["nope", "nice try!", "sounds about right", "i dont think so!", "nice try!"]

###########################################       initialize audio for listening in background ####
r = sr.Recognizer()
m = sr.Microphone()


###########################################   GLOBAL FUNCTIONS #####################################################################

# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    print("Speak Now . . .")
    r.energy_threshold = energyThres
    r.dynamic_energy_threshold = False
    speaking=False
    
    # Call LED lights here
    ard.ledListening()
    

    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)  # phrase_time_limit=3)
        
        
        
        try:
            # Call LED lights here
            ard.ledAll()
            print("Recognising....")
            text = r.recognize_google(audio, language='en')
            global user_input
            user_input = text
            print(text)
            playScript("audio/Short Marimba desecending.mp3")
            return text
            

        except Exception as e:
            print("ask etti: Exception " + str(e))
            return "0x01"
        

def playScript(url):
    mixer.init()
    mixer.music.set_volume(0.3)
    mixer.music.load(url)
    mixer.music.play()
   
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
    

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

    mixer.music.set_volume(1.0)
    mixer.music.load(filename)
    mixer.music.play()

    # Create an MP3 object
    # Specify the directory address to the mp3 file as a parameter
    #audio = MP3("temp.mp3")
    # Contains all the metadata about the mp3 file
    #audio_info = audio.info
    #length_in_secs = int(audio_info.length)
    #hours, mins, seconds = convert(length_in_secs)
    #sleep(seconds+0.9)
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)


########################################################### QUIZ SCREEN ###########################################################################
############ SUBJECT1: RHYMING WORDS
class QuizWorker2(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    time = pyqtSignal(str)
    
    def countdown(self, time_sec=600):
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            time_sec -= 1
            self.time.emit(timeformat)
        
        self.finished.emit()
        print("stop")
        

class QuizWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    button = pyqtSignal(str,str)
    lcd = pyqtSignal(int)
    image = pyqtSignal(str)


    def Quiz1(self):

        global user_input, score
        response = user_input
        self.button.emit("", "")
        self.progress.emit("Direction: Identify whether the words shown are rhyming or not rhyming. Answer by clicking the button or with your voice saying the word 'YES' if it's rhyming and 'NO' if it's not rhyming words.")
        speak("Identify whether the words shown are rhyming or not rhyming. You can answer by clicking the buttons or with your voice. saying the word yes if it's rhyming. and no if it's not.")
        ard.lookDown()
        sleep(1)
        speak("ready?")
        sleep(1)
        def q1():
            self.progress.emit("1. Car - bar")
            speak("number 1. car. bar")

        def q2():
            self.progress.emit("2. sail - tail")
            speak("number 2. sail. tail")

        def q3():
            self.progress.emit("3. can - cat")
            speak("number 3. can. cat")

        def q4():
            self.progress.emit("4. pig - wig")
            speak("number 4. pig. wig")

        def q5():
            self.progress.emit("5. map - hut")
            speak("number 5. map. hut")
        
        self.button.emit("NO", "YES")

        q1()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Perfect!")
                #self.countResponse()
                break

            elif user_input == "no":
                ard.notNod()
                speak("uhm")
                break

        user_input = ""
        
        
        q2()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Great!")
                #self.countResponse()
                
                break

            elif user_input == "no":
                ard.notNod()
                speak("uh oh!")
                break

        user_input = ""

        
        q3()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
                score += 1
                self.lcd.emit(score)
                
                ard.nod()
                speak("Great!")
                #self.countResponse()
                
                break

            elif user_input == "yes":
                ard.notNod()
                speak("nope!")
                break

        user_input = ""

        
        q4()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Great!")
                #self.countResponse()
                
                break

            elif user_input == "no":
                ard.notNod()
                speak("nice try!")
                break

        user_input = ""
        
        
        q5()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                #self.countResponse()
                
                break

            elif user_input == "yes":
                ard.notNod()
                speak("nope!")
                break

        user_input = ""

        self.progress.emit(f"You've got {score} out of 5.")
        speak(f"You've got {score} out of 5.")
        self.lcd.emit(score)
        if score >= 3:
            self.progress.emit("You did well! :)")
            speak("You did well, ooh wooh!")
            ard.nod()
            
        elif score < 3:
            self.progress.emit("Try again Next Time :(")
            speak("Try again Next Time")

        sleep(3)
        self.finished.emit()
        score = 0

################################## SUBJECT1: SENTENCES AND NON SENTENCES
    #Sentences and NSn sentences
    def Quiz2(self):

        global user_input, score
        self.button.emit("", "")
        
        self.progress.emit("Direction: Say 'Yes' if the given item is a sentence and 'No' if it is a Non-sentence.\n")
        speak("Say YES. if the given item is a sentence. and NO. if it is a Non-sentence.")
        sleep(1)
        speak("ready?")
        sleep(1)
        def q1():
            self.progress.emit("1. My name is Paula Marie.")
            speak("number 1. My name is Paula Marie.")

        def q2():
            self.progress.emit("2. my wonderful pet")
            speak("number 2. my wonderful pet")

        def q3():
            self.progress.emit("3. Anna’s new phone")
            speak("number 3. Anna’s new phone")

        def q4():
            self.progress.emit("4. What is your name?")
            speak("number 4. What is your name?")

        def q5():
            self.progress.emit("5. her father’s house")
            speak("number 5. her father’s house")

        def q6():
            self.progress.emit("6. The children are playing.")
            speak("number 6. The children are playing.")

        def q7():
            self.progress.emit("7. Ramon sings a song.")
            speak("number 7. Ramon sings a song.")

        def q8():
            self.progress.emit("8. I am sorry.")
            speak("number 8. I am sorry.")

        def q9():
            self.progress.emit("9. playing the piano")
            speak("number 9. playing the piano")

        def q10():
            self.progress.emit("10. Selling some apples")
            speak("number 10. selling some apples")
        self.button.emit("NO", "YES")
        
        
        ard.lookDown()
        q1()
        ard.lookStraight()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Perfect!")
                break

            elif user_input == "no":
                ard.notNod()
                speak("uhm nice try")
                break

        user_input = ""

        ard.lookDown()
        q2()
        ard.lookStraight()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Great!")
                break

            elif user_input == "yes":
                ard.notNod()
                speak("uh oh!")
                break

        user_input = ""

        q3()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Great!")
                break

            elif user_input == "yes":
                ard.notNod()
                speak("Nope!")
                break

        user_input = ""

        q4()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Great!")
                break

            elif user_input == "no":
                ard.notNod()
                speak("nice try!")
                break

        user_input = ""

        q5()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                break

            elif user_input == "yes":
                ard.notNod()
                speak("Nope!")
                break

        user_input = ""

        q6()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                break

            elif user_input == "no":
                ard.notNod()
                speak("Nope!")
                break



        user_input = ""

        q7()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                break

            elif user_input == "no":
                ard.notNod()
                speak("Nope!")
                break

        user_input = ""

        q8()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "yes":
                
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                break

            elif user_input == "no":
                ard.notNod()
                speak("Nope!")
                break

        user_input = ""

        q9()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
               
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                break

            elif user_input == "yes":
                ard.notNod()
                speak("nice try!")
                break

        user_input = ""


        q10()
        while True:
            #response = ask_ettibot().lower()
            if user_input == "no":
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Well Done!")
                break

            elif user_input == "yes":
                ard.notNod()
                speak("nice try!")
                break

        user_input = ""


        self.progress.emit(f"You've got {score} out of 10.")
        speak(f"You've got {score} out of 10.")

        if score >= 5:
            self.progress.emit("You did well! :)")
            ard.nod()
            speak("You did well!")


        elif score < 5:
            self.progress.emit("Try again Next Time :(")
            ard.nod()
            speak("Try again Next Time")

        sleep(3)
        self.finished.emit()
        score = 0
        
    #Polite Expression
    def Quiz3(self):
        print("Quiz 3")
        
        global user_input, score

        self.button.emit(" ", " ")
        self.progress.emit('''Direction: Match the expressions shown on
        the screen with their appropriate responses.. You can answer by speaking
        the appropriate response or by clicking the button''')
        
        speak('Match the expressions shown on the screen with their appropriate responses.')
        speak('You can answer by speaking the appropriate response or by clicking the button.')
        
        sleep(1)
        speak("ready?")
        sleep(1)
        
        def q1():
            self.progress.emit("1. Good morning!")
            self.button.emit("You're welcome", "Good morning")
            speak("number 1. good morning!")
            
        def q2():
            self.progress.emit("2. May I go out?")
            self.button.emit("Yes you may", "Good morning")
            speak("number 2. may i go out?")
            
        def q3():
            self.progress.emit("3. Thank you for helping me!")
            self.button.emit("Yes please open it","You're welcome")
            speak("number 3. Thank you for helping me!")
        

        def q4():
            self.progress.emit("4. Would you like me to open this for you?")
            self.button.emit("Good Morning", "Yes please open it")
            speak("number 4. Would you like me to open this for you?")
        
        q1()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            tokenize_ans = word_tokenize(user_input)
            bestAns = ['good morning', 'morning','good']
            notAns = ['you\'re welcome', 'welcome','you\'re']
            if any(i in tokenize_ans for i in bestAns):
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Perfect!")
                #self.countResponse()
                break

            elif user_input == "you're welcome":
                ard.notNod()
                speak("uhm")
                break

        user_input = ""
        
        
        q2()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            tokenize_ans = word_tokenize(user_input)
            bestAns = ['yes you may', 'yes','you may']
            notAns = ['good morning', 'good','morning']
            if any(i in tokenize_ans for i in bestAns):
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Great!")
                #self.countResponse()
                
                break

            elif any(i in tokenize_ans for i in notAns):
                ard.notNod()
                speak("uh oh!")
                break

        user_input = ""

        q3()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            tokenize_ans = word_tokenize(user_input)
            bestAns = ['you\'re welcome', 'welcome','you\'re']
            notAns = ['yes please open it', 'yes please','open it', 'open']
            if any(i in tokenize_ans for i in bestAns):
                score += 1
                self.lcd.emit(score)
                
                ard.nod()
                speak("Right!")
                #self.countResponse()
                
                break

            elif any(i in tokenize_ans for i in notAns):
                ard.notNod()
                speak("nope!")
                break

        user_input = ""

        
        q4()
        ard.lookDown()
        ard.ledListening()
        while True:
            #response = ask_ettibot().lower()
            tokenize_ans = word_tokenize(user_input)
            bestAns = ['yes please open it', 'yes please','open it', 'open']
            notAns = ['good morning', 'good','morning']
            if any(i in tokenize_ans for i in bestAns):
                score += 1
                self.lcd.emit(score)
                ard.nod()
                speak("Correct!")
                #self.countResponse()
                
                break

            elif any(i in tokenize_ans for i in notAns):
                ard.notNod()
                speak("nice try!")
                break
            

        user_input = ""

        self.progress.emit(f"You've got {score} out of 4.")
        speak(f"You've got {score} out of 4.")
        self.lcd.emit(score)
        if score >= 3:
            self.progress.emit("You did well! :)")
            speak("You did well, ooh wooh!")
            ard.nod()

        elif score < 3:
            self.progress.emit("Try again Next Time :(")
            speak("Try again Next Time")

        sleep(3)
        self.finished.emit()
        score = 0
        
        
        
        self.finished.emit()
        

class QuizMain(QWidget):  # second screen showing the quiz screen
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Q1.ui', self)
        self.btnFalse.clicked.connect(self.falseButton)
        self.btnTrue.clicked.connect(self.trueButton)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor)
        
        
    def runTimer(self):
        # Step 2: Create a QThread object
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker2 = QuizWorker2()
        # Step 4: Move worker to the thread
        self.worker2.moveToThread(self.thread2)
        self.thread2.started.connect(self.worker2.countdown)

        self.worker2.finished.connect(self.thread2.quit)
        self.worker2.finished.connect(self.worker2.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.worker2.time.connect(self.updateScreenTime)
        #self.worker2.progress.connect(self.updateScreen)
        # Step 6: Start the thread
        self.thread2.start()

        # Final resets
        #self.btnAbout.setEnabled(False)

        self.thread2.finished.connect(
            lambda: self.timerLabel.setText("00:00")
        )
        

    def run(self):
        global flag, subjectLesson
        flag = "Quiz"
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = QuizWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        #self.subjectNow()
        if subjectLesson == "Rhyming and Non-Rhyming":
            self.thread.started.connect(self.worker.Quiz1)
            self.quiz_Title.setText("Rhyming and Non-Rhyming")
            self.runTimer()
            

        elif subjectLesson == "Sentence":
            self.thread.started.connect(self.worker.Quiz2)
            self.quiz_Title.setText("Sentence and Non-Sentence")
            self.runTimer()
            
        elif subjectLesson == "Express":
            self.thread.started.connect(self.worker.Quiz3)
            self.quiz_Title.setText("Polite Expression")
            self.runTimer()

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateScreen)
        self.worker.button.connect(self.updateButton)
        self.worker.lcd.connect(self.updateLCD)
        self.worker.image.connect(self.updateImage)

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

    def updateLCD (self, num):
        self.lcd.display(num)

    def updateButton (self, opt1, opt2):
        self.btnFalse.setText(opt1)
        self.btnTrue.setText(opt2) #
        
    def updateImage(self, url='images/polite expression.png'):
        self.pixmap = QPixmap()
        self.setMinimumSize(1, 1)
        self.pixmap.load(url)
        self.subtitle_2.setPixmap(self.pixmap)
        self.subtitle_2.setScaledContents(True)
        
        #self.button.setIcon(QtGui.QIcon('myImage.jpg')) #Adding Icon as Image to button
        #self.button.setIconSize(QtCore.QSize(200,200)) #

    def updateScreen(self, message):
        self.subtitle_2.setText(message)
        self.subtitle_2.setAlignment(Qt.AlignCenter)
        #self.subject_Title.setText(subject)
        
    
    def updateScreenTime(self, time):
        self.timerLabel.setText(time)
        

    def falseButton(self):
        btnFalse = self.btnFalse.text()
        global user_input
        user_input = btnFalse.lower()
        print(user_input)

    def trueButton(self):
        btnTrue = self.btnTrue.text()
        global user_input
        user_input = btnTrue.lower()
        print(user_input)


#############################################   LEARNING TASKS

class QuizScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Quizzes.ui', self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor)
        
        self.btnStart.clicked.connect(self.showMenu)
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnExpress.clicked.connect(self.showExpress)
        self.btnRhyming.clicked.connect(self.showRhyme)
        self.btnSentence.clicked.connect(self.showSentence)

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        #self.stop_listening = r.listen_in_background(m, self.callback)


    def showRhyme(self):
        global subjectLesson
        subjectLesson = self.btnRhyming.text()
        
        self.btnRhyming.setEnabled(False)
        speak(self.btnRhyming.text())
        #self.threadTopic.stop()
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()


    def showExpress(self):
        global subjectLesson
        subjectLesson = "Express"
        
        self.btnExpress.setEnabled(False)
        speak(self.btnExpress.text())
        
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()


    def showSentence(self):
        global subjectLesson
        subjectLesson = "Sentence"
        
        self.btnSentence.setEnabled(False)
        speak(self.btnSentence.text())
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()

    def showStories(self):
        global subjectLesson
        subjectLesson = "Stories"
        #self.Topics.setText(self.btnStories.text())
        self.btnStories.setEnabled(False)
        speak(self.btnStories.text())
        self.subj = QuizMain()
        self.subj.show()
        self.subj.run()
        self.close()

    def showMenu(self):
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "MainMenu"
        
        self.btnMenu.setEnabled(False)
        
        self.window = MainMenu()
        self.window.show()
        self.window.run()
        self.hide()

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


############################################################################################ SCREENS ###################################################################

############ SUBJECT1: RHYMING WORDS
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    image = pyqtSignal(str)
    button = pyqtSignal(bool)
    title = pyqtSignal(str)
    timer = pyqtSignal(str)

    def subjectNow(self):
        global timer, user_input
        subject = "Rhyming and Non-rhyming"
        #speaks(self.script)
        #self.updateScreen(subject)
        #speaks("Try to read the sets of words below")
        ard.lookStraight() 
        self.progress.emit("In this lesson, you will learn about Rhyming Words.")
        
        speak("In this lesson, you will learn about Rhyming Words.")
        ard.lookDown()
        sleep(0.5)
        
        self.progress.emit("Words are formed by combining the letters of the alphabet.")
        ard.lookStraight()
        speak("Words are formed by combining the letters of the alphabet.")
        
        sleep(0.5)
        
        self.progress.emit("It is important to remember that the English alphabet is composed of 26 letters with 5 vowels and 21 consonants.")
        speak("It is important to remember that the English alphabet is composed of")
        speak("26 letters, 5 vowels and 21 consonants.")

        self.progress.emit("\n")
        self.image.emit('images/rhyming.png')
        ard.lookDown()
        speak("vowels are like, ah. ae. e. oh. oooh.")
        speak("Now, consonants are like alphabets without vowels. Such as b,c,d,f,g, and so on.")
        
        sleep(0.7)
        
        self.progress.emit("By combining some of these letters, words may be formed.")
        ard.lookStraight()
        speak("By combining some of these letters, words may be formed.")
        
        sleep(0.8)
        
        self.progress.emit("Some of these words include net, one, pen, and red. Some words have the same or similar ending sounds.")
        ard.lookDown()
        speak("Some of these words include net, one, pen, and red.")
        ard.lookStraight()
        speak("Some words have the same or similar ending sounds.")
        
        sleep(0.3)
        
        self.progress.emit("They are called rhyming words. At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        ard.lookDown()
        speak("They are called rhyming words.")
        
        sleep(0.9)
        
        ard.lookDown()
        speak("At the end of the lesson, you are expected")
        ard.lookStraight()
        speak("to recognize rhyming words in nursery rhymes, poems or songs heard.")
        
        sleep(0.3)
        
        
        self.progress.emit("House - Mouse")
        speak("Try to read the example below.")
        self.button.emit(False)
        ard.lookDown()
        
        user_input = ""
        ard.ledListening()
        while True:
            response = user_input
            if any (i in response for i in ["house mouse", "mouse", "house"]):
                ard.nod()
                speak("Perfect!")
                self.progress.emit("Perfect")
                #self.countResponse()
                break
            
            elif flag != "Subject":
                self.finished.emit()
                break
            
            

        self.progress.emit("Set - Net")
        speak("Try this one.")
        ard.lookDown()

        user_input = ""
        ard.ledListening()
        while True:
            response = user_input
            if any (i in response for i in ["set net", "set", "net"]):
                ard.nod()
                speak("Great!")
                self.progress.emit("Great!")
                #self.countResponse()
                break
            
            elif flag != "Subject":
                self.finished.emit()
                break

        self.progress.emit("Big - Small")
        speak("How about this one?")
        ard.lookDown()

        user_input = ""
        ard.ledListening()
        while True:
            response = user_input
            if any (i in response for i in  ["big small","big", "small"]):
                ard.nod()
                speak("Well done!")
                self.progress.emit("Well done!")
                break
            
            elif flag != "Subject":
                self.finished.emit()
                break

        self.image.emit('images/rhymeSets.png')
        speak("Notice the sounds of the words?")
        ard.lookDown()
        sleep(0.6)
        speak("Sets A and B are considered as rhyming words")
        sleep(0.3)
        ard.lookStraight()
        speak("while set C is not.")
        
        sleep(2)
        ard.nod()
        speak("That's all for today's discussion. Thank you for listening!")
        
        ########## The Learning Task 1
        """
        speak("Let's take a test if you understand the lesson.")
        sleep(1)
        speak("are you ready?")
        
        user_input = ""
        while True:
            response = user_input
            if any (i in response for i in  ["ready","yup", "yes"]):
                speak("great!")
                break
        
        sleep(1)
        
        speak("But. Before anything else. Do you have your notebook?")
        
        user_input = ""
        while True:
            response = user_input
            if any (i in response for i in  ["ready","yup", "yes", "yep"]):
                speak("great!")
                break
            
            elif response == "no":
                self.progress.emit("Say 'DONE' if you have your notebook.")
                speak("Please prepare your notebook.")
                sleep(1)
                speak("Once you've got your notebook. Just say the magic word. Done")
                
            elif response == "done":
                speak("great!")
                break
            
        sleep(2)
        speak("On your notebook, write numbers from 1 to 5")
        
        #self.image.emit()
        speak("Now. you see what's on the screen?")
        sleep(1.3)
        
        speak("You have to match the pictures which have the same ending sounds.")
        speak("Just write the letters of your answers in your notebook")
        
        sleep(1)
        speak("I'm giving you 3 minutes to finish it.")
        
        speak("sounds fair?")
        while True:
            response = ask_ettibot().lower()
            if any (i in response for i in  ["ready","yup", "yes", "sure"]):
                speak("great!")
                timer = 180 #180 secs equivalent to 3 minutes
                break
            
            elif response == "no":
                speak("Hmm, how about 10 minutes?")
                
                while True:
                    response = ask_ettibot().lower()
                    if any (i in response for i in  ["okay","ok","yup", "yes", "sure"]):
                        timer = 600 #600 secs equivalent to 3 minutes
                        speak("okay, 10 minutes!")
                        break
            
                    elif response == "no":
                        speak("Sorry, but I think 10 minutes is too much for just 5 items, right?")
                        speak("Alright.")
                        timer = 600 #600 secs equivalent to 3 minutes
                        break
                    
        self.progress.emit("Just say done, once you are finished earlier on time.")
        speak("Just say done, once you are finished earlier on time.")
        speak("Timer. starts. now.")
        print(f"Timer is set to {timer}")
        #emit timer here
        
        while True:
            response = ask_ettibot().lower()
            if response == "done":
                speak("great!")
                break
            
            elif timer == 0:
                speak("Time is up!")
                break
        
        speak("Please hand it over to your parent or guardian and have it check")
        speak("Here's the key to correction.")
        
        """
        self.finished.emit()

    ############ SUBJECT2: SENTENCES AND NON-SENTENCES
    def subjectNow2(self):
        subject = "Sentences and Non Sentences"

        ard.lookStraight()
        self.progress.emit("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
        speak("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
        ard.lookDown()
        
        self.title.emit("Sentence")
        self.progress.emit("A sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate. It begins with a capital letter and ends with a period ( . ), a question mark ( ? ), or an exclamation point ( ! ).")
        ard.lookStraight()
        speak("A sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate.")
        ard.lookDown()
        speak("It begins with a capital letter and ends with a period, a question mark, or an exclamation point.")
        ard.lookStraight()
        self.image.emit("images/sentence2.png")
        speak("Study the sample sentences below.")
        
        ard.lookDown()
        speak("1. Ella plays the piano.")
        speak("Ella is the subject, while plays the piano is the predicate.")
        speak("2. The sun rises in the east.")
        speak("The sun is the subject, and rises in the east is the predicate.")
        speak("3. The garden is beautiful.")
        speak("The garden is the subject, and is beautiful is the predicate.")
        
        ard.lookStraight()
        speak("Now.")
        
        self.title.emit("Non Sentence")
        
        self.progress.emit("A non-sentence, like a phrase, is also a group of words. Unlike a sentence, it does not tell a complete thought or idea. It may just be the subject or the predicate.")
        
        
        speak("A non-sentence, like a phrase, is also a group of words.")
        ard.lookDown()
        speak("Unlike a sentence, it does not tell a complete thought or idea.")
        speak("It may just be the subject or the predicate.")

        self.image.emit("images/sentence3.png")
        speak("Study the sample non-sentences below.")
        ard.lookStraight()
        speak("playing the piano.")
        ard.lookDown()
        speak("wide garden.")
        speak("Jayson's dog.")
        speak("Ray and may.")
        speak("sets in the west.")
        speak("flying a kite.")
        speak("Unlike a sentence, the examples below do not give complete thoughts or meanings.")
        ard.nod()
        speak("That's all for today's video, thank you for listening!")
        self.finished.emit()


    ############ SUBJECT3: Short Stories or Poems
    def subjectNow3(self):

        def emitStory():
            self.progress.emit("The New Toys")
            speak("The New Toys")
            ard.lookDown()
            self.image.emit("images/new toys.png")
            speak("Jay and Joy have new toys.")
            
            speak("Jay has a new toy car. It is small but shiny.")
            speak("Meanwhile,Joy has a new doll. It is big and beautiful.")
            speak("Their Tita May gave these gifts to them during their birthday.")
            speak("She hid them behind the table to surprise them.")
            speak("They hurriedly looked for the hidden gifts.")
            speak("When they saw them, they immediately opened them.")
            ard.nod()
            speak("They jumped for joy when they saw their new toys. They were just what they wished for.")
            speak("They thanked and kissed their Tita. They love their new toys.")

        def q1():
            self.progress.emit("Who received gifts during their birthday?")
            speak("Who received gifts during their birthday?")

        def q2():
            self.progress.emit("Who gave them the gifts?")
            speak("Who gave them the gifts?")

        def q3():
            self.progress.emit("Where did she hide the gifts?")
            speak("Where did she hide the gifts?")

        def q4():
            self.progress.emit("What gifts did they receive?")
            speak("What gifts did they receive?")

        def q5():
            self.progress.emit("What did they do when they found the gifts?")
            speak("What did they do when they found the gifts?")

        subject = "Short Stories"
        #speaks(self.script)
        #speaks("Try to read the sets of words below")
        ard.lookStraight()
        self.progress.emit("Are you familiar with short stories and poems?")
        speak("Are you familiar with short stories and poems?")
        ard.lookDown()

        self.progress.emit("You've possibly read and listened to different stories and poems")
        speak("You've possibly read and listened to different stories and poems,")
        ard.lookStraight()

        self.progress.emit("such as fairy tales and other bedtime stories.")
        speak("such as fairy tales and other bedtime stories.")
        ard.lookDown()
        
        self.progress.emit("These stories and poems tell us what the characters feel and do. They may also teach us important lessons in life.")
        speak("These stories and poems tell us what the characters feel and do.")
        speak("They may also teach us important lessons in life.")
        ard.lookStraight()

        self.progress.emit("Now. Listen to this story.")
        speak("Now. Listen to this story,")
        
        self.title.emit("The New Toys")
        ard.lookDown()
        emitStory()
        ard.lookStraight()
        
        self.title.emit(subject)
        speak("Try to answer these questions")
        self.button.emit(False)

        q1()
        ard.lookDown()
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["jay", "joy", "jay and joy", "j n joy"]):
                speak("Perfect!")
                ard.nod()
                self.progress.emit("Jay and Joy")
                sleep(3)
                self.countResponse()
                break

            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                q1()
                continue


        q2()
        ard.lookDown()
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["tita", "auntie","may", "tita may"]):
                speak("Perfect!")
                self.progress.emit("Tita May")
                ard.nod()
                sleep(3)
                self.countResponse()
                break

            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("sure!")
                emitStory()
                q2()
                continue


        q3()
        ard.lookDown()
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["table", "behind the table"]):
                speak("Great!")
                self.progress.emit("Behind the Table")
                ard.nod()
                sleep(3)
                self.countResponse()
                break

            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("no problem!")
                emitStory()
                q3()
                continue



        q4()
        ard.lookDown()
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["toy car and doll", "car", "doll", "toy"]):
                speak("Perfect!")
                self.progress.emit("Toy Car and Doll")
                ard.nod()
                sleep(3)
                self.countResponse()
                break

            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                q4()
                emitStory()
                continue



        q5()
        ard.lookDown()
        while True:
            response = ask_ettibot().lower()
            if any(i in response for i in ["jumped", "jump", "jumped for joy"]):
                speak("Well done!")
                self.progress.emit("They Jumped for Joy")
                ard.nod()
                sleep(3)
                self.countResponse()
                break

            elif any(i in response for i in ["can you repeat the story", "repeat story"]):
                speak("okay!")
                emitStory()
                continue

        ard.nod()
        speak("That's all for today's video, thank you for listening!")
        self.finished.emit()



############ SUBJECT4: Polite Expressions
    def subjectNow4(self):
        subject = "Polite Expressions"
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        ard.lookStraight()
        self.progress.emit("Politeness is one of the characteristics that you should have.")
        speak("Politeness is one of the characteristics that you should have.")
        ard.lookDown()
        
        self.progress.emit("There are lots of ways on how one can show politeness.")
        speak("There are lots of ways on how one can show politeness.")
        ard.lookStraight()
        
        self.progress.emit("Saying po and opo is one of these ways")
        speak("Saying")
        speak("po at opo", "tl")
        ard.lookUp()
        speak("is one of these ways.")
        ard.lookDown()

        self.progress.emit("Also, you can show politeness using appropriate words or expressions in different events.")
        speak("Also, you can show politeness using appropriate words or expressions in different events.")
        ard.lookStraight()
        
        self.progress.emit("At the end of the lesson, you are expected to use respond appropriately to polite expressions in greetings, leave takings, expressing gratitude and apology, asking permission, and offering help. ")
        speak("At the end of the lesson, you are expected to use respond appropriately to polite expressions in greetings")
        ard.lookDown()
        speak("leave takings, expressing gratitude and apology, asking permission, and offering help.")


        self.progress.emit("Read the example shown on screen.")
        speak("Now, Listen to this conversation")
        ard.lookDown()
        
        self.progress.emit("\n")
        self.image.emit('images/polite expression.png')

        sleep(2)
        playScript('audio/PoliteExpress.mp3')

        speak("Notice the highlighted words.")
        speak("Good afternoon, Thank you very much. and You are welcome are examples of polite greetings. that you may use in talking to other people. ")


        self.progress.emit("That's All, Thank you for listening!")
        ard.nod()
        speak("That's all for today's discussion, thank you for listening!")

        sleep(3)
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

    def stopThread (self):
        self.finished.emit()


######################################################## DYNAMIC SCREEN SUBJECT #########################################################
class Subject(QWidget):  # second screen showing the discussion screen
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/subject.ui', self)
        self.btnStart.clicked.connect(self.run)
        self.btnMenu.clicked.connect(self.showMenu)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor) 


    def updateImage(self, url='images/polite expression.png'):
        self.pixmap = QPixmap()
        self.setMinimumSize(1, 1)
        self.pixmap.load(url)
        self.subtitle_2.setPixmap(self.pixmap)
        self.subtitle_2.setScaledContents(True)

        #self.setCentralWidget(label)
        #self.resize(pixmap.width(), pixmap.height(300))

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

    def buttonState(self, show=True):
        if show:
            self.btnStart.show()
            self.btnMenu.show()

        else:
            self.btnStart.hide()
            self.btnMenu.hide()
            
    def updateTitle(self, title):
        self.subject_Title.setText(title)

    def run(self):
        global flag, subjectLesson
        flag = "Subject"
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        #self.subjectNow()
        if subjectLesson == "Rhyming Words":
            self.thread.started.connect(self.worker.subjectNow)
            self.subject_Title.setText(subjectLesson)

        if subjectLesson == "Sentence":
            self.thread.started.connect(self.worker.subjectNow2)
            self.subject_Title.setText("Sentences and Non-Sentences")

        if subjectLesson == "Stories":
            self.thread.started.connect(self.worker.subjectNow3)
            self.subject_Title.setText("Short Stories")

        if subjectLesson == "Express":
            self.thread.started.connect(self.worker.subjectNow4)
            self.subject_Title.setText("Polite Expressions")

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateScreen)
        self.worker.button.connect(self.buttonState)
        self.worker.image.connect(self.updateImage)
        self.worker.title.connect(self.updateTitle)
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


######################################################## TOPICS Screen  #####################################################################
class topics(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/topics.ui', self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor)
        #sleep(duration)
        self.btnMenu.clicked.connect(self.showMenu)

        self.btnExpress.clicked.connect(self.showExpress)
        self.btnRhyming.clicked.connect(self.showRhyme)
        self.btnSentence.clicked.connect(self.showSentence)
        self.btnStories.clicked.connect(self.showStories)
        self.btnStart.clicked.connect(self.startLesson)

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        #self.stop_listening = r.listen_in_background(m, self.callback)

    def startLesson(self):
        self.showRhyme()

    def run(self):
        global flag
        flag = "Topics"
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        #self.stop_listening = r.listen_in_background(m, self.callback)


    def showRhyme(self):
        global subjectLesson
        subjectLesson = self.btnRhyming.text()
        self.btnRhyming.setEnabled(False)
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
        self.btnExpress.setEnabled(False)
        speak(self.btnExpress.text())
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()


    def showSentence(self):
        global subjectLesson
        subjectLesson = "Sentence"
        self.Topics.setText(self.btnSentence.text())
        self.btnSentence.setEnabled(False)
        speak(self.btnSentence.text())
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()

    def showStories(self):
        global subjectLesson
        subjectLesson = "Stories"
        self.Topics.setText(self.btnStories.text())
        self.btnStories.setEnabled(False)
        speak(self.btnStories.text())
        self.subj = Subject()
        self.subj.show()
        self.subj.run()
        self.close()

    def showMenu(self):
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "MainMenu"
        self.btnMenu.setEnabled(False)
        self.window = MainMenu()
        self.window.show()
        self.window.run()
        self.hide()

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


#############################################################  TRANSLATE Screen  #######################################################
class TranslateWorker2(QObject):
    finished2 = pyqtSignal()
    button2 = pyqtSignal()
    progress2 = pyqtSignal(str,str)
    result2 = pyqtSignal()

    def run(self):
        self.progress2.emit(" ","You can translate English words to Filipino and vise versa. ")
        speak("You can translate English words to Filipino and vise versa. ")
        self.progress2.emit(" ","Try saying KAMUSTA")
        speak("Try saying")
        speak("kamusta", "tl")
        sleep(3)
        
        
        self.finished2.emit()
        #self.translateNow()

class TranslateWorker(QObject):
    finished = pyqtSignal()
    button = pyqtSignal()
    progress = pyqtSignal(str,str)
    result = pyqtSignal()
    
    def translateNow(self):
        #Translate: the bot will get user input then recognize if the input is english or tagalog
        #then bot will convert the input into opposite language and speak the output
        #speak("You can try saying. Translate, then the word you want to translate. For example, translate Goodmorning")

        while flag == "Translate":
            if flag != "Translate":
                print("flag is not Translate")
                self.finished.emit()
                break

            print("Flag: " +flag)
            query = ask_ettibot().lower()
            
            #word = query
            #prefix = 'translate'
            
            #print(word[word.startswith(prefix) and len(prefix):])
            #stippedWord = word[word.startswith(prefix) and len(prefix):]
            detected_lang = translator.detect(query)
            
            #if any(i in query for i in ["translate", "salin wika", "translation"]):
            
            if query == "cancel":
                print("flag is not Translate")
                self.finished.emit()
                break
            
            if query != '0x01':
                try:
                    if detected_lang.lang == 'en':
                        translate_text = translator.translate(query, dest='tl')
                        print(f"Translation: {translate_text.text}")
                        output = translate_text.text
                        self.progress.emit(query, output)
                        speak(translate_text.text, 'tl')


                    elif detected_lang.lang == 'tl':
                        translate_text = translator.translate(query, dest='en')
                        print(f"Translation: {translate_text.text}")
                        output = translate_text.text
                        self.progress.emit(query, output)
                        speak(translate_text.text, 'en')


                except Exception as e:
                    print("Translate Exception " + str(e))
                    speak("Please Try again.")
                    continue
            

           
class TranslatorScreen(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Translator.ui', self)
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnHow.clicked.connect(self.showHow)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor)
        
        global flag
        flag = "Translate"
        
        #self.start_button()
        #checkPlaying()
        #checkPlaying()
        #speak("at sasabihin ko sa wikang filipino ay. Magandang Umaga!", "tl")
        #self.t1 = threading.Thread(name = "TranslateLoop", target=self.translateNow)
        #self.t1.setDaemon(True)


        # start listening in the background (note that we don't have to do this inside a `with` statement)
        #self.stop_listening = r.listen_in_background(self.m, self.callback)


    def updateScreen(self, inputTxt="User Input", outputTxt="Translation"):
        self.transInput.setText(f"You: {inputTxt}")
        self.transOutput.setText(f"AI: {outputTxt}")

    def updateButton(self):
        self.btnHow.setEnabled(True)

    def showHow(self):
        # Step 2: Create a QThread object
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker2 = TranslateWorker2()
        # Step 4: Move worker to the thread
        self.worker2.moveToThread(self.thread2)
        #self.subjectNow()


        self.thread2.started.connect(self.worker2.run)

        self.worker2.finished2.connect(self.thread2.quit)
        self.worker2.finished2.connect(self.worker2.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.worker2.progress2.connect(self.updateScreen)
        self.worker2.button2.connect(self.updateScreen)
        self.worker2.result2.connect(self.showHow)

        # Step 6: Start the thread
        self.thread2.start()
    
        # Final resets
        self.btnHow.setEnabled(False)
        
        self.thread2.finished.connect(
            lambda: self.btnHow.setEnabled(True)
        )


    def showMenu(self):
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "MainMenu"
        self.btnMenu.setEnabled(False)
        self.window = MainMenu()
        self.window.show()
        self.window.run()
        self.hide()


    def run(self):
        global flag
        flag = "Translate"

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = TranslateWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        #self.subjectNow()


        self.thread.started.connect(self.worker.translateNow)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateScreen)
        self.worker.button.connect(self.updateScreen)
        self.worker.result.connect(self.showHow)

        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.thread.finished.connect(
            lambda: self.showMenu()
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

            if any (i in text for i in ["translate"]):
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

        elif 0x01 in query:
            print(query)


        else:
            res = np.random.choice(
                ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you."])
            speak(res)
            print(query)








###################### MAIN MENU SCREEN ###################################################################################
class MenuWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    time = pyqtSignal()
    translate = pyqtSignal()
    
    def updateTime(self):
        global flag
        while True:
            self.time.emit()
            if flag != "MainMenu":
                self.finished.emit()
                break
            
            if flag == "Translate":
                self.finished.emit()
            
            

class MenuWorker2(QObject):
    finished2 = pyqtSignal()

    def run(self):
        ard.nod()
        res = np.random.choice(["I am designed to teach basic english for my children and communicate with people, just like you!", "I am Artificial Intelligence English Tutor"])
        speak(res)
        ard.lookStraight()
        self.finished2.emit()




class MainMenu(QWidget):
    def __init__(self):
        global flag
        flag = "MainMenu"
        threading.current_thread().name = "Menu"
        super().__init__()
        uic.loadUi('screens/welcome.ui', self) # MainWindow.ui
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor) 
        #activeScreen = "MainMenu"
        # Create and connect widgets
        self.btnTopics.clicked.connect(self.runTopics)
        self.btnQuiz.clicked.connect(self.runQuiz)
        self.btnTranslate.clicked.connect(self.runTranslate)
        self.btnAbout.clicked.connect(self.runAbout)

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        #self.stop_listening = r.listen_in_background(m, self.callback)


    def run(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = MenuWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        #self.subjectNow()
        self.thread.started.connect(self.worker.updateTime)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.time.connect(self.updateScreenTime)
        self.worker.translate.connect(self.runTranslate)
        # Step 6: Start the thread
        self.thread.start()
        
        self.thread.finished.connect(
            lambda: self.gotoScreen()
        )
        
        
    def gotoScreen(self):
        global flag
        if flag == 'Translate':
            print("go to translate")
            #self.runTranslate()
            #self.MainThrd.close()
            #speak(self.btnTranslate.text())
            self.translate = TranslatorScreen()
            self.translate.show()
            self.translate.run()
            self.hide()
            
        elif flag == 'Topics':
            print("go to Topics")
            self.runTopics()
            
        
    def stop(self):
        self._go = False
        

    def runTopics(self):
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Topics"
        self.btnTopics.setEnabled(False)
        #self.MainThrd.join()
        #speak(self.btnTopics.text())
        self.lesson = topics()
        self.lesson.show()
        self.hide()
        #self.close()
        #self.my_loop("topics")
        #MainThrd.join()
        #MainMenu=False

    def updateScreenTime(self):
        x = datetime.datetime.now()
        Day = x.strftime("%A")
        Month = x.strftime("%B")
        DayInt = x.strftime("%d")

        Hour = x.strftime("%I")
        Minute = x.strftime("%M")
        Seconds =  x.strftime("%S")
        Meridian =  x.strftime("%p")


        self.date.setText(f"{Month}, {DayInt}")
        self.day.setText(Day)
        self.time.setText(f"{Hour}:{Minute}:{Seconds} {Meridian}")

    def updateScreen(self, text):
        self.Title.setText(text)

    def runQuiz(self):
        # self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Quiz Screen"
        self.btnQuiz.setEnabled(False)
        speak(self.btnQuiz.text())
        #self.MainThrd.close()
        #speak("Quizzes")
        self.quiz = QuizScreen()
        self.quiz.show()
        self.hide()
        #self.close()


    def runTranslate(self):
        #self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Translate"
        self.btnTranslate.setEnabled(False)
        
        #self.close()


    def runAbout(self):
        # Step 2: Create a QThread object
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker2 = MenuWorker2()
        # Step 4: Move worker to the thread
        self.worker2.moveToThread(self.thread2)
        self.thread2.started.connect(self.worker2.run)

        self.worker2.finished2.connect(self.thread2.quit)
        self.worker2.finished2.connect(self.worker2.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        #self.worker2.progress.connect(self.updateScreen)
        # Step 6: Start the thread
        self.thread2.start()

        # Final resets
        self.btnAbout.setEnabled(False)

        self.thread2.finished.connect(
            lambda: self.btnAbout.setEnabled(True)
        )

    def gotoMenu(self):
        self.show()

class splashWorker (QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        for i in range (2, 20):
            self.progress.emit(i)
            sleep(0.01)
            
        sleep(0.5)
        
        for i in range (20, 30):
            self.progress.emit(i)
            sleep(0.01)
            
        sleep(0.5)
        
        for i in range (30, 70):
            self.progress.emit(i)
            sleep(0.01)
            
        sleep(1)
        
        for i in range (70, 100):
            self.progress.emit(i)
            sleep(0.01)
            
        for i in range (100, 101):
            self.progress.emit(i)
            sleep(0.01)
            
        sleep(2)
        
        self.finished.emit()
        
            
class SplashScreen(QWidget):
    def __init__(self):
        global flag
        flag = "Splash"
        threading.current_thread().name = "Menu"
        super().__init__()
        uic.loadUi('/home/pi/ai-thesis/src/screens/splashscreen.ui', self) # splashscreen.ui
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()  # opening window in maximized size
        self.setCursor(Qt.BlankCursor)  
        #activeScreen = "MainMenu"
        # Create and connect widgets

    def run(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = splashWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateBar)
        # Step 6: Start the thread
        self.thread.start()

        self.thread.finished.connect(
            lambda: self.gotoMenu()
        )

        self.thread.finished.connect(
            lambda: self.close()
        )

    def updateBar(self, i):
        self.progressBar.setValue(i)

    def gotoMenu(self):
        self.window = MainMenu()
        self.window.run()
        self.window.show()


def myThread():
    speak("Good Day, learner!")
    ard.ledAll()
    
    while "thread":
        if flag == "Quiz":
            print(f"Score: {score}")
            
        if flag == "Subject":
            print(f"Timer: {timer}")

        print(f"Learner's Name: {learner_name}")
        print(f"User voice: {user_input}")
        print(f"Counter: {counter}")
        print(f"FLAG: {flag}")
        print(f"Subject: {subjectLesson}")
        print(threading.enumerate())
        sleep(1)
        try:
            pass

        except KeyboardInterrupt:
            sys.exit(0)
            

# this is called from the background thread
def callback(recognizer, audio):
    #ard.ledListening()
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + text)
        
        global user_input
        user_input = text
        stripWords = word_tokenize(text)
        greetWords = ["hello", "hi"]
        stopWords = ["ai", "madam", "tutor", "athena", "thesis"]
        #print (text)
        
        if any (i in stripWords for i in greetWords) and flag == "MainMenu":
            res = np.random.choice(
                ["hello!", "hi!", "yes?", "hello?"])
            ard.nod()
            speak(res)
            
        
        if any (i in stripWords for i in stopWords):
            result = [i for i in stripWords if not any([e for e in stopWords if e in i])] #this code removes the stopWords from stripWords
            recognizedWords(result)
        
        #if any (i in text for i in ["ai", "madam", "tutor", "athena", "thesis", "hi", "hello"]):
            #playScript("audio/Short Marimba Notification Ding.mp3")
        #    recognizedWords(text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def recognizedWords(text):
    global flag
    
    if flag == "MainMenu":
        response = ask_ettibot().lower()
        query = word_tokenize(response)
        #print("Speaking: "+str(speaking))
        #window = MainMenu ()
        #self.updateScreen(f"You: {query}")
        #print(query)
        #if window.isVisible():
        #    print("Main Menu is Visible")

        #elif splash.isVisible():
        #    print("Splash is Visible")

        # topics
        if any(i in query for i in ["topic", "topics", "lessons", "lesson", "learn"]):
            flag = "Topics"
            print (flag)

        # quiz
        elif any(i in query for i in ["quiz", "quizzes", "play"]):
            flag = "Quiz Screen"
            print (flag)
           
        # translate
        elif any(i in query for i in ["translate", "translation"]):
            flag = "Translate"
            print (flag)

        # about me
        elif "about" in query:
            flag = "About"
            print (flag)


        # respond politely
        elif any(_ in query for _ in ["thank", "thanks"]):
            res = np.random.choice(
                ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
            speak(res)


        # respond politely
        elif any(_ in query for _ in ["good morning", "morning"]):
            ard.nod()
            res = np.random.choice(
                ["Good morning human", "good morning too!"])
            speak(res)
            
        # respond politely
        elif any(i in query for i in ["hi", "hello"]):
            ard.nod()
            ard.lookStraight()
            res = np.random.choice(["hi", "hello!", "What do you need?"])
            speak(res)
            
        elif any(i in query for i in ["hear"]):
            ard.nod()
            ard.lookStraight()
            res = np.random.choice(["yes?", "I can hear you"])
            speak(res)
            

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
            #echo "export OPENAI_API_KEY='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'" >> ~/.zshrc
            #openai.api_key = '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'
            #openai.api_key = os.getenv("OPENAI_API_KEY")
            #response = openai.Completion.create(
            #  engine="text-davinci-002",
            #  prompt=query,
            #  temperature=0.9,
            #  max_tokens=60,
            # top_p=1.0,
            #  frequency_penalty=0.5,
            #  presence_penalty=0.6,
            #  stop=["Human:", "AI:"]
            #)
            
            #print(response.choices[0].text)
            #speak(response.choices[0].text)
            
            res = np.random.choice(
                ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you.", "Sorry?", "Can you repeat that?"])
            speak(res)
            print(query)



def main():
    app = QApplication(sys.argv)
    print("Mainthread: Started")

    splash = SplashScreen()
    splash.run()
    splash.show()
    
    #window = MainMenu()
    #window.run()
    #window.show()
    
    with m as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = energyThres
        
    stop_listening = r.listen_in_background(m, callback) #phrase_time_limit=10

    #MainThrd.join()

    #Enumerate Running Threads
    checkThread = threading.Thread(name="Enumerate", target=myThread)
    checkThread.setDaemon(True)
    checkThread.start()


    sys.exit(app.exec_())

if __name__ == '__main__':
    #Main Thread
    try:
        main()
        
    except KeyboardInterrupt as k:
        sys.exit()
        sys.exit(app.exec_())
        print(k)

