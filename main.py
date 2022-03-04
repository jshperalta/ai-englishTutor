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
from playsound import playsound

import pyglet
import sys
import defines.speakandrecognize as snr
import speech_recognition as sr
import arduinoServo as ard

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import *

translator= Translator()

pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
logging.basicConfig(format="%(message)s", level=logging.INFO)

global activeScreen, speaking, duration, flag
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

# start listening in the background (note that we don't have to do this inside a `with` statement)
#stop_listening = r.listen_in_background(m, ask_ettibot)

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
    playsound(filename)
    song = MP3(filename)
    songLength = song.info.length
    duration = songLength
    #print(songLength)
    #print(duration)
    #sleep(duration)
    #music = pyglet.media.load(filename, streaming=False)
    #music.play()    
    #os.remove(filename)  # remove temporary file
    #return speaking, duration
    
    
    
def checkPlaying():
        while pygame.mixer.music.get_busy():
          time.sleep(0.01)
            
            
# ------CLASSES ----- SCREENS

class Subject(QDialog):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/subject.ui', self)
        self.btnMenu.clicked.connect(self.showMenu)
        print("Main Thread")
        
        #self.subjectLesson()
    def run(self):
        global flag
        flag = "Subject"
        #self.t1.join()
        
    def subjectLesson(self):
        print("Sub Thread")
        self.subject = "Rhyming Words"
        self.subject_Title.setText("Rhyming Words")
        self.script = "Words are formed by combining the letters of the alphabet. It is important to remember that the English alphabet is composed of 26 letters with 5 vowels and 21 consonants. vowels are like, ah. ae. ē. oh. oooh. Now, consonants are like alphabets without vowels. Such as b,c,d,f,g, and so on. By combining some of these letters, words may be formed. Some of these words include net, one, pen, and red.Some words have the same or similar ending sounds. They are called rhyming words.At the end of the lesson, you are expected to recognize rhyming words in nursery rhymes, poems or songs heard."
        self.script2 = "vowels are like, ah. ae. ē. oh. oooh"
        self.script2_2 = "a. e. i. o. u"
        #self.speaks(self.script)
        #self.speaks("Try to read the sets of words below")
        self.updateText(self.script)
        speak(self.script)
        
    def updateText(self, text):
        self.subtitle_2.setText(text)
        
        
        
        #self.hide()
        
    #def speaks(self, text, lang="en"):  # here audio is var which contain text
        
        
        
    def showMenu(self):
        speak(self.btnMenu.text())
        lesson.show()
        self.hide()

        

class topics(QDialog):  # second screen showing the lesson and activity
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
        #self.listen()
        
        
    def showRhyme(self):
        self.rhyme = Subject()
        self.rhyme.show()     
        self.hide()
        speak(self.btnRhyming.text())
        #self.t1 = threading.Thread(target=self.rhyme.subjectLesson)
        #self.t1.setDaemon(True)
        #self.t1.start()
        
        subjectTitle = self.btnRhyming.text()
        return subjectTitle

        
    def showMenu(self):
        self.Topics.setText(self.btnMenu.text())
        speak(self.btnMenu.text())
        window.show()
        self.hide()
        
    def showExpress(self):
        self.Topics.setText(self.btnExpress.text())
        speak(self.btnExpress.text())
        #self.hide()
        
        
    def showSentence(self):
        
        self.Topics.setText(self.btnSentence.text())
        speak(self.btnSentence.text())
        #self.hide()
        
    def showStories(self):
       
        self.Topics.setText(self.btnStories.text())
        speak(self.btnStories.text())
        #self.hide()
    


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
        self.t1 = threading.Thread(target=self.translateNow)
        self.t1.setDaemon(True)

        
    def updateScreen(self, inputTxt="User Input", outputTxt="Translation"):
        self.transInput.setText(inputTxt)
        self.transOutput.setText(outputTxt)
        
    def showMenu(self):
        global flag
        flag = "MainMenu"
        #window = MainMenu()
        window.show()
        self.hide()
        t3 = threading.Thread(target=my_loop)
        t3.setDaemon(True)
        t3.start()
        
    def start_button(self):
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
                
            elif "none" in query:
                print(query)
                

            else:
                res = np.random.choice(
                    ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you."])
                speak(res)
                print(query)
                
            #else:
            #    continue
                
         
        

class QuizScreen(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/Quizzes.ui', self)
    

        # video recorder
        #self.my_countdown_timer.timeout.connect(self.my_timer)
        #self.my_countdown_timer.start(1000)
        self.btnStart.clicked.connect(self.show_Quiz)
        self.btnMenu.clicked.connect(self.showMenu)
        self.btnExpress.clicked.connect(self.show_Quiz)
        self.btnRhyming.clicked.connect(self.show_Quiz)
        self.btnSentence.clicked.connect(self.show_Quiz)
        #self.counter = 5
        #self.lcd_TIMER.display(self.counter)

    def my_timer(self):
        self.counter -= 1
        if (self.counter == 0):
            quiz1.show_Quiz2(self)
        self.lcd_TIMER.display(self.counter)

    def show_Quiz(self):
        #self.my_countdown_timer.stop()
        #self.quiz = quiz1()
        #self.quiz.show()
        #self.hide()
        speak("Quiz number 1")
        
    def showMenu(self):
        global flag
        flag = "MainMenu"
        #window = MainMenu()
        window.show()
        self.hide()
        t3 = threading.Thread(target=my_loop)
        t3.setDaemon(True)
        t3.start()
           

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


              
class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('screens/welcome.ui', self) # MainWindow.ui
        #self.setupUi()
        #self.showMaximized()  # opening window in maximized size
        #self.transWidget.hide()
        #global activeScreen
        
        #activeScreen = "MainMenu"
        # Create and connect widgets
        self.btnTopics.clicked.connect(self.runTopics)
        self.btnQuiz.clicked.connect(self.runQuiz)
        self.btnTranslate.clicked.connect(self.runTranslate)
        self.btnAbout.clicked.connect(self.runAbout)
        
        
        # Step 6: Start the thread   
        
    def runTopics(self):
        speak("topics")
        self.lesson = topics()
        self.lesson.show()     
        self.hide()
        query = self.btnTopics.text()
        return query
        
    def runQuiz(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        speak("You have selected Quiz")
        self.quiz = QuizScreen()
        self.quiz.show()
        self.hide()
        
    def runTranslate(self):
        self.translate = TranslatorScreen()
        self.translate.show()
        self.translate.start_button()
        self.hide()
        
    def runAbout(self):
        ard.nod()
        speak("I'm Etti, I am designed to teach basic english for my children and communicate with people, just like you!")
        ard.lookStraight()
        
    def gotoMenu(self):
        self.show()
        

        
def my_loop():
    global flag
    # Final resets
    #self.longRunningBtn.setEnabled(False)
    #self.thread.finished.connect(
    #    lambda: self.longRunningBtn.setEnabled(True)
    #)
    #self.thread.finished.connect(
    #    lambda: self.stepLabel.setText("Long-Running Step: 0")
    #)
    speak("Main Menu...")
    #LOOP Listening state
    flag = "MainMenu"
    while True:
        flag = "MainMenu"
        print(f"FLAG is: {flag}")
        #print("Speaking: "+str(speaking))
        query = ask_ettibot().lower()
        #print(query)
        #if window.isVisible():
        #    print("Main Menu is Visible")
            
        #elif splash.isVisible():
        #    print("Splash is Visible")
        
        # topics
        if any(i in query for i in ["topic", "topics", "show topics", "what's the lessons"]):
            window.runTopics()
            break

        # quiz
        elif any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
            self.window.runQuiz()
            break
            
        # translate
        elif flag == "Translate":
            print("flag is Translate")
            break
        
        elif any(i in query for i in ["translate", "salin wika", "translation"]):
            if translatr.isVisible():
                continue
            else:
                flag = "Translate"
                window.runTranslate()
                window.hide()
                break
            
        
        # about me
        elif "about" in query:
            window.showAbout() 


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
            ard.nod()
            
        elif "none" in query:
            print(query)
            

        else:
            res = np.random.choice(
                ["Sorry, I don't understand what you said.", "I dont know that yet.", "Sorry, I didn't catch that.", "I didn't get that, but I heard you."])
            speak(res)
            print(query)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = MainMenu()
    #window.show()
  
   
    
    #t2 = threading.Thread(target=menuloop)
    #t2.setDaemon(True)
    t = threading.Thread(target=my_loop)
    t.setDaemon(True)
    t.start()

    #start threading
    
    #t2.start()
    #t2.join()
    #t.join()
    
    #splash = SplashScreen()
    #splash.show()
    #splash.progress()
    print("Mainthread: Started")
    window = MainMenu()
    #splash.finish(window)
    window.show()
    translatr = TranslatorScreen()
    lesson = topics()
    subject = Subject()
    #translate.translateNow()
    
    #topics = Topics()
    #quiz = Quiz()
    #translate = Translate()
    #about = About()
    
    sys.exit(app.exec_())
