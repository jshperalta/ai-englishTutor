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



# ------FUNCTIONS

# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    print("Speak Now . . .")
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False
    speaking=False
    
    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)  # phrase_time_limit=3)
        # Call LED lights here
        
        try:
            # Call LED lights here
            print("Recognising....")
            text = r.recognize_google(audio, language='en')
            print(text) 

        except Exception as e:
            print("ask etti: Exception " + str(e))
            return "none"

    return text


# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    global my_answer, counter, user_input, respond, speaking, duration
    counter += 1
    # Call LED lights here
    speaking = True
    # calling this function requests that the background listener stop listening
    #stop_listening(wait_for_stop=True)
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    #pygame.mixer.music.load(filename)
    #pygame.mixer.music.play()
    #mixer.music.load(filename)
    playsound(filename, True)
    song = MP3(filename)
    songLength = song.info.length
    duration = songLength
    #print(songLength)
    print(duration)
    #sleep(duration)
    #music = pyglet.media.load(filename, streaming=False)
    #music.play()    
    #os.remove(filename)  # remove temporary file
    #return speaking, duration
    
    
def checkPlaying():
        while pygame.mixer.music.get_busy():
          time.sleep(0.01)
            
            
# ------CLASSES ----- SCREENS

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        
        
        
class Subject(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/subject.ui', self)
        self.btnStart.clicked.connect(self.run)
        self.btnMenu.clicked.connect(self.showMenu)
        
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
        self.btnStart.setEnabled(False)
        global flag
        flag = "Subject"
        #self.t1 = threading.Thread(name = "TranslateLoop", target=self.subjectNow)
        #self.t1.setDaemon(True)
        #self.t1.start()
        #MainThrd.stop()
        if subjectLesson == "Rhyme":
            self.subjectNow()
        
        if subjectLesson == "Express":
            self.subjectNow2()
            
        if subjectLesson == "Sentence":
            self.subjectNow3()
            
        if subjectLesson == "Stories":
            self.subjectNow4()
        
    def updateScreen(self, message):
        self.subtitle_2.setText(message)
        
    def subjectNow(self):
        subject = "Rhyming Words"
        self.subject_Title.setText(subject)
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        self.updateScreen("In this lesson, you will learn about Rhyming Words.")
        self.speak("In this lesson, you will learn about Rhyming Words.")
        self.updateScreen("Words are formed by combining the letters of the alphabet.")
        self.speak("Words are formed by combining the letters of the alphabet.")
        self.updateScreen("It is important to remember that the English alphabet is composed of 26 letters with 5 vowels and 21 consonants.")
        self.speak("It is important to remember that the English alphabet is composed of 26 letters, with 5 vowels and 21 consonants.")
        self.updateScreen("Vowels: \nAa  Ee Ii Oo Uu")
        self.speak("vowels are like, ah. ae. ē. oh. oooh.")
        self.updateScreen("Consonants: \nBb Cc Dd Ff Gg Hh Jj Kk Ll Mm Nn Pp Qq Rr Ss Tt Vv Ww Xx Yy Zz.")
        self.speak("Now, consonants are like alphabets without vowels. Such as b,c,d,f,g, and so on.")
        self.updateScreen("By combining some of these letters, words may be formed.")
        self.speak("By combining some of these letters, words may be formed.")
        self.updateScreen("Some of these words include net, one, pen, and red.Some words have the same or similar ending sounds.")
        self.speak("Some of these words include net, one, pen, and red.Some words have the same or similar ending sounds.")
        self.updateScreen("They are called rhyming words.At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        self.speak("They are called rhyming words.At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard.")
        self.updateScreen("SET A: \nHouse - Mouse.")
        self.speak("Try to read the example below.")
        
        while True:
            response = ask_ettibot().lower()     
            if response == "house mouse":
                self.speak("Perfect!")
                self.updateScreen("Perfect")
                self.countResponse()
                break
        
        self.updateScreen("SET B: \nSet - Net.")
        self.speak("Try this one.")
        
        while True:
            response = ask_ettibot().lower()
            if response == "set net":
                self.speak("Great!")
                self.updateScreen("Perfect")
                self.countResponse()
                break
        
        self.updateScreen("SET C: \nBig - Small.")
        self.speak("How about this one?")
        
        while True:
            response = ask_ettibot().lower()   
            if response == "big small":
                self.speak("Well done!")
                self.updateScreen("Perfect")
                break
            
        self.subjectNow3()
        
        
    def subjectNow3(self):
        subject = "Sentences and Non Sentences"
        self.subject_Title.setText(subject)
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        self.updateScreen("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
        self.speak("When words are combined, you will form a group of words which may either be a sentence or a non-sentence.")
     
        self.updateScreen("Sentence\n\nA sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate. It begins with a capital letter and ends with a period ( . ), a question mark ( ? ), or an exclamation point ( ! ).")
        self.speak("A sentence is a group of words. It tells a complete thought or idea. It is composed of a subject and a predicate.")
        self.speak("It begins with a capital letter and ends with a period, a question mark, or an exclamation point.")
        
        self.updateScreen("1. Ella plays the piano.\n2. The sun rises in the east.\n3. The garden is beautiful.")
        self.speak("Study the sample sentences below.")
        self.speak("Ella plays the piano.")
        self.speak("The sun rises in the east.")
        self.speak("The garden is beautiful.")
        
        self.updateScreen("Non-Sentences\n\nA non-sentence, like a phrase, is also a group of words. Unlike a sentence, it does not tell a complete thought or idea. It may just be the subject or the predicate.")
        self.speak("A non-sentence, like a phrase, is also a group of words.")
        self.speak("Unlike a sentence, it does not tell a complete thought or idea.")
        self.speak("It may just be the subject or the predicate.")
        
        self.updateScreen("1. playing the piano\n2. wide garden\n3. Ray and May")
        self.speak("Study the sample non-sentences below.")
        self.speak("playing the piano")
        self.speak("wide garden")
        self.speak("Ray and May")
        self.speak("Unlike a sentence, the examples below do not give complete thoughts or meanings.")
        
        self.speak("That's all for today's video, thank you for listening!")
        self.close()
            
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
        self.speak("topics")
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

        

class topics(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/topics.ui', self)
        #self.showMaximized()  # opening window in maximized size
        activeScreen = "topics"
        #sleep(duration)
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnExpress.clicked.connect(self.showExpress)
        self.btnRhyming.clicked.connect(self.showRhyme)
        self.btnSentence.clicked.connect(self.showSentence)
        self.btnStories.clicked.connect(self.showStories)
        self.btnStart.clicked.connect(self.startLesson)
        
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
            r.energy_threshold = 4000
            
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)
        
        
    def showRhyme(self):
        global subjectLesson
        subjectLesson = "Rhyme"
        #self.threadTopic.stop()
        self.subj = Subject()
        self.subj.show()
        self.close()
        
        
    def showExpress(self):
        global subjectLesson
        subjectLesson = "Express"
        self.Topics.setText(self.btnExpress.text())
        speak(self.btnExpress.text())
        self.subj = Subject()
        self.subj.show()
        self.close()
        
        
    def showSentence(self):
        global subjectLesson
        subjectLesson = "Sentence"
        self.Topics.setText(self.btnSentence.text())
        speak(self.btnSentence.text())
        self.subj = Subject()
        self.subj.show()
        self.close()
        
    def showStories(self):
        global subjectLesson
        subjectLesson = "Stories"
        self.Topics.setText(self.btnStories.text())
        speak(self.btnStories.text())
        self.subj = Subject()
        self.subj.show()
        self.close()
        
    def showMenu(self):
        global flag
        flag = "Topics"
        window = MainMenu()
        
        window.show()
       
        #self.hide()
        self.close()
        
    def updateScreen(self, text):    
        self.Topics.setText(text)
        
    def speak(self, text, lang="en"):  # here audio is var which contain text
        # Call LED lights here
        speaking = True
        tts = gTTS(text=text, lang=lang)
        filename = 'temp.mp3'
        tts.save(filename)
        playsound(filename, False)
        #pygame.mixer.music.load(filename)
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
          #  print("busy")
        
    # this is called from the background thread
    def callback(self, recognizer, audio):
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
                self.speak(res)

                
            # respond politely
            elif any(_ in query for _ in ["good morning", "morning"]):
                res = np.random.choice(
                    ["Good morning human", "good morning too!"])
                self.speak(res)
                

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                
                self.speak(res)
                self.updateScreen(f"Etti: {res}")
                ard.nod()
                
            elif "none" in query:
                print(query)
                
            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you.", "Sorry?"])
                self.speak(res)
                print(query)
    


class TranslatorScreen(QDialog): 
    def __init__(self):
        super().__init__()
        uic.loadUi('Translator.ui', self)
        activeScreen = "Translator"
        self.btnMenu.clicked.connect(self.showMenu)
        #self.start_button()
        #checkPlaying()
        #checkPlaying()
        #speak("at sasabihin ko sa wikang filipino ay. Magandang Umaga!", "tl")
        self.t1 = threading.Thread(name = "TranslateLoop", target=self.translateNow)
        self.t1.setDaemon(True)

        
    def updateScreen(self, inputTxt="User Input", outputTxt="Translation"):
        self.transInput.setText(inputTxt)
        self.transOutput.setText(outputTxt)
        
    def showMenu(self):
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
        self.t1.start()
        
        
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
                
         
        

class QuizScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Quizzes.ui', self)
        
        self.btnStart.clicked.connect(self.showMenu)
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnExpress.clicked.connect(self.showMenu)
        self.btnRhyming.clicked.connect(self.showMenu)
        self.btnSentence.clicked.connect(self.showMenu)
        
        self.speak("Quizzes")
        
        #initialize audio for listening in background
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 4000
            
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)
        
        
    def showMenu(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "MainMenu"
        window = MainMenu()
        #Thread 1
        #MyLoop = threading.Thread(name="MenuLoop", target=window.my_loop)
        #MyLoop.setDaemon(True)
        #MyLoop.start()
        window.show()
        self.close()
        
    def updateScreen(self, text):    
        self.Title.setText(text)
        
    def speak(self, text, lang="en"):  # here audio is var which contain text
        # Call LED lights here
        speaking = True
        tts = gTTS(text=text, lang=lang)
        filename = 'temp.mp3'
        tts.save(filename)
        playsound(filename, False)
        #pygame.mixer.music.load(filename)
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
          #  print("busy")
    
    # this is called from the background thread
    def callback(self, recognizer, audio):
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
        
        if flag == "Quiz":
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
                self.runTopics()
                self.stop_listening(wait_for_stop=False)

            # quiz
            elif any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
                self.runQuiz()
                self.stop_listening(wait_for_stop=False)
                
            # translate
            elif flag == "Translate":
                print("flag is Translate")
               
            
            elif any(i in query for i in ["translate", "salin wika", "translation"]):
                if translatr.isVisible():
                    pass
                else:
                    flag = "Translate"
                    self.runTranslate()
                    self.hide()
                    self.stop_listening(wait_for_stop=False)
            
            # about me
            elif "about" in query:
                self.showAbout() 


            # respond politely
            elif any(_ in query for _ in ["thank", "thanks"]):
                res = np.random.choice(
                    ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])
                self.speak(res)

                
            # respond politely
            elif any(_ in query for _ in ["good morning", "morning"]):
                res = np.random.choice(
                    ["Good morning human", "good morning too!"])
                self.speak(res)
                

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                
                self.speak(res)
                self.updateScreen(f"Etti: {res}")
                ard.nod()
                
            elif "none" in query:
                print(query)
                
            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you.", "Sorry?"])
                self.speak(res)
                print(query)

              
class MainMenu(QWidget):
    def __init__(self):
        global flag
        flag = "MainMenu"
        threading.current_thread().name = "Menu"
        super().__init__()
        uic.loadUi('screens/welcome.ui', self) # MainWindow.ui
        
        #activeScreen = "MainMenu"
        # Create and connect widgets
        self.btnTopics.clicked.connect(self.runTopics)
        self.btnQuiz.clicked.connect(self.runQuiz)
        self.btnTranslate.clicked.connect(self.runTranslate)
        self.btnAbout.clicked.connect(self.runAbout)
    
        self.updateScreen("Main Menu...")
        self.speak("Main Menu...")
        
    
        #initialize audio for listening in background
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 4000
            
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = r.listen_in_background(m, self.callback)

        
    def runTopics(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Topics"
        #self.MainThrd.join()
        self.speak("topics")
        self.lesson = topics()
        self.lesson.show()
        self.hide()
        #self.close()
        #self.my_loop("topics")
        #MainThrd.join()
        MainMenu=False
      
        
    def updateScreen(self, text):    
        self.Title.setText(text)
        
    def runQuiz(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Quiz"
        #self.MainThrd.close()
        #self.speak("Quizzes")
        self.quiz = QuizScreen()
        self.quiz.show()
        #self.hide()
        self.close()
        
        
    def runTranslate(self):
        self.stop_listening(wait_for_stop=False)
        global flag
        flag = "Translate"
        #self.MainThrd.close()
        translate = TranslatorScreen()
        translate.show()
        translate.run()
        self.hide()
        #self.close()
        
        
    def runAbout(self):
        ard.nod()
        self.speak("I'm Etti, I am designed to teach basic english for my children and communicate with people, just like you!")
        ard.lookStraight()
        
    def gotoMenu(self):
        self.show()
        
    def speak(self, text, lang="en"):  # here audio is var which contain text
        # Call LED lights here
        speaking = True
        tts = gTTS(text=text, lang=lang)
        filename = 'temp.mp3'
        tts.save(filename)
        playsound(filename, False)
        #pygame.mixer.music.load(filename)
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
          #  print("busy")
    
    # this is called from the background thread
    def callback(self, recognizer, audio):
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
                lesson = topics(threading.thead)
                lesson.show()
                self.close()

            # quiz
            elif any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
                self.stop_listening(wait_for_stop=False)
                flag = "Quiz"
                #self.MainThrd.close()
                #self.speak("Quizzes")
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
                self.speak(res)

                
            # respond politely
            elif any(_ in query for _ in ["good morning", "morning"]):
                res = np.random.choice(
                    ["Good morning human", "good morning too!"])
                self.speak(res)
                ard.lookLeft()
                

            # respond politely
            elif any(i in query for i in ["hi", "hello", "can you hear me"]):
                res = np.random.choice(
                    ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
                
                self.speak(res)
                self.updateScreen(f"Etti: {res}")
                ard.lookRight()
                
            elif any(i in query for i in ["up", "look up"]):
                ard.lookUp()
                ard.lookStraight()
                
            elif any(i in query for i in ["down", "look down"]):
                ard.lookDown()
                ard.lookStraight()
                
            elif any(i in query for i in ["left", "look left"]):
                ard.lookLeft()
                ard.lookStraight()
                
            elif any(i in query for i in ["right", "look right"]):
                ard.lookRight()
                ard.lookStraight()
                
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
                self.speak(res)
                print(query)
                
   
def myThread():
    while True:
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
    
    print("Mainthread: Started")
    window = MainMenu()
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
    
    
