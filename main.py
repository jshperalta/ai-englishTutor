import logging
import random
import sys
import time
# MAIN CODE
import os
import time
import datetime
import numpy as np
import pygame
from time import sleep
from googletrans import Translator
import threading
import queue
from gtts import gTTS
from mutagen.mp3 import MP3

import pyglet
import sys
import defines.speakandrecognize as snr
import speech_recognition as sr

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic import *

translator= Translator()
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
logging.basicConfig(format="%(message)s", level=logging.INFO)

global activeScreen, speaking, duration
duration = 0
my_answer = ""
language = ""
counter = 0
p = 0
activeScreen = ""
translatedWord = ""
r = sr.Recognizer()
m = sr.Microphone()
speaking = False

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
            print("Exception " + str(e))
            return "none"

    return text, speaking


# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, ask_ettibot)

# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    global my_answer, counter, user_input, respond, speaking, duration
    counter += 1
    # Call LED lights here
    speaking = True
    # calling this function requests that the background listener stop listening
    stop_listening(wait_for_stop=True)
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    #mixer.music.load(filename)
    song = MP3(filename)
    songLength = song.info.length
    duration = songLength
    #print(songLength)
    #print(duration)
    #sleep(duration)
    #music = pyglet.media.load(filename, streaming=False)
    #music.play()    
    #os.remove(filename)  # remove temporary file
    return speaking, duration
    
    
    
def checkPlaying():
        while pygame.mixer.music.get_busy():
          time.sleep(0.01)
            
            
# ------CLASSES ----- SCREENS
class topics(QDialog):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/topics.ui', self)
        speak(
            "Let us learn something new!You can choose between rhyming words, sentences, short stories, and polite expressions. Which one should we try? ")
        #self.showMaximized()  # opening window in maximized size
        activeScreen = "topics"
        
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnExpress.clicked.connect(self.showExpress)
        self.btnRhyming.clicked.connect(self.showRhyme)
        self.btnSentence.clicked.connect(self.showSentence)
        self.btnStories.clicked.connect(self.showStories)
        
        
        
    def showMenu(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.Topics.setText(self.btnMenu.text())
        speak(self.btnMenu.text())
        window.show()
        self.hide()
        
    def showExpress(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.Topics.setText(self.btnExpress.text())
        speak(self.btnExpress.text())
        #self.hide()
        
    def showRhyme(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.Topics.setText(self.btnRhyming.text())
        speak(self.btnRhyming.text())
        #self.hide()
        
    def showSentence(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.Topics.setText(self.btnSentence.text())
        speak(self.btnSentence.text())
        #self.hide()
        
    def showStories(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.Topics.setText(self.btnStories.text())
        speak(self.btnStories.text())
        #self.hide()


class Translator(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Translator.ui', self)
        #self.showMaximized()  # opening window in maximized size
        activeScreen = "Translator"
        self.btnMenu.clicked.connect(self.showMenu)
        #checkPlaying()
        #checkPlaying()
        #speak("at sasabihin ko sa wikang filipino ay. Magandang Umaga!", "tl")
        
    def updateScreen(self, inputTxt="User Input", outputTxt="Translation"):
        self.transInput.setText(inputTxt)
        self.transOutput.setText(outputTxt)
        
    def showMenu(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        speak(self.btnMenu.text())
        window.show()
        self.hide()
        
        
    #def translateNow(query):
        #Translate: the bot will get user input then recognize if the input is english or tagalog
        #then bot will convert the input into opposite language and speak the output
        


class quiz(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Quizzes.ui', self)
        speak("Quiz. number. one")
        self.my_countdown_timer = QTimer()
        activeScreen = "quiz"

        # video recorder
        self.my_countdown_timer.timeout.connect(self.my_timer)
        self.my_countdown_timer.start(1000)
        self.btn_1.clicked.connect(self.show_Quiz2)
        self.counter = 5
        self.lcd_TIMER.display(self.counter)

    def my_timer(self):
        self.counter -= 1
        if (self.counter == 0):
            quiz1.show_Quiz2(self)
        self.lcd_TIMER.display(self.counter)

    def show_Quiz(self):
        self.my_countdown_timer.stop()
        self.quiz = quiz2()
        self.quiz.show()
        self.hide()
        snr.speak("Quiz number 2")
           

class SplashScreen(QSplashScreen):  # first window
    def __init__(self):
        super().__init__()
        self.showMaximized()  # opening window in maximized size
        uic.loadUi('screens/splashscreen.ui', self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)  # Removes the frame of the window
        global activeScreen
        activeScreen = "SplashScreen"
        

    def progress(self):
        # speak("Welcome button clicked")
        for i in range(100):
            sleep(0.03)
            self.progressBar.setValue(i)
            

def my_loop():
    #LOOP Listening state
    
    while True:
        print("Speaking: "+str(speaking))
        query = ask_ettibot().lower()
        
        #if window.isVisible():
        #    print("Main Menu is Visible")
            
        #elif splash.isVisible():
        #    print("Splash is Visible")
        
        # topics
        if any(i in query for i in ["topics", "show topics", "what's the lessons"]):
            window.runTopics()

        # quiz
        elif any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
            window.runQuiz()
            
        # translate
        elif any(i in query for i in ["translate", "salin wika", "translation"]):
            translatr.show()
            window.close()
            
            if len(query.split()) > 1: # has more than 1 word
                word = query.replace("translate", '')
                #translatr.updateScreen(word)
                print(word)
                detected_lang = translator.detect(word)
                print(detected_lang.lang)
                
                try: 
                    if detected_lang.lang == 'en':
                        translate_text = translator.translate(word, dest='tl')
                        print(translate_text)
                        output = translate_text.text
                        speak(translate_text.text, 'tl')
                        translatr.updateScreen(word, output)

                    elif detected_lang.lang == 'tl':
                        translate_text = translator.translate(word, dest='en')
                        print(translate_text)
                        output = translate_text.text
                        speak(translate_text.text, 'en')
                        translatr.updateScreen(word, output)
                        
                except Exception as e:
                    print("Exception " + str(e))
                    return "Please say which word to translate"
                
                
            else:
                speak("You can try saying. Translate, then the word you want to translate. For example, translate Goodmorning")
        

        # about me
        elif "about" in query:
            window.showAbout()

        elif "none" in query:
            print(query)
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

        else:
            speak("Sorry, I don't understand what you said. Please try again.")
            print(query)
           
              
class MainMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('screens/welcome.ui', self)
        #self.setupUi()
        #self.showMaximized()  # opening window in maximized size
        #self.transWidget.hide()
        #global activeScreen
        speak("Main Menu...")
        #activeScreen = "MainMenu"
        # Create and connect widgets
        self.btnTopics.clicked.connect(self.runTopics)
        self.btnQuiz.clicked.connect(self.runQuiz)
        self.btnTranslate.clicked.connect(self.runTranslate)
        self.btnAbout.clicked.connect(self.runAbout)
        
        
    def runTopics(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        speak("Topics")
        self.lesson = topics()
        self.lesson.show()
        if self.lesson.isVisible():
            self.hide()

        else:
            self.lesson.show()
                
        #self.hide()
        
    def runQuiz(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        speak("You have selected Quiz")
        self.translate = Translator()
        self.translate.show()
        self.hide()
        
    def runTranslate(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        speak("You can try saying. Translate, then the word you want to translate. For example, translate Goodmorning")
        self.translate = Translator()
        self.translate.show()
        self.translate.updateScreen()
        self.hide()
        
    def runAbout(self):
        speak("I'm Etti, I am designed to teach basic english for my children and communicate with people, just like you!")
        

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        for i in range(threadCount):
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(i)
            # 3. Call start()
            pool.start(runnable)
            
            
    def gotoMenu():
        self.show()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = MainMenu()
    #window.show()
    
    
    
    #t2 = threading.Thread(target=MainMenu)
    #t2.setDaemon(True)
    

    #start threading
    t = threading.Thread(target=my_loop)
    t.setDaemon(True)
    t.start()
    #t2.start()
    #t2.join()
    #t.join()
    
    #splash = SplashScreen()
    #splash.show()
    #splash.progress()
    
    window = MainMenu()
    translatr = Translator()
    #splash.finish(window)
    window.show()
    
    sleep(duration)
    speak("mic test")
    print(duration)
    sleep(duration)
    speak("Hello")
    sleep(duration)
    speak("World")
    #translate.translateNow()
    
    #topics = Topics()
    #quiz = Quiz()
    #translate = Translate()
    #about = About()
    
    sys.exit(app.exec())
