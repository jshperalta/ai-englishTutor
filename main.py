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

import sys
import defines.speakandrecognize as snr

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic import *

translator = Translator()
pygame.mixer.init()
logging.basicConfig(format="%(message)s", level=logging.INFO)

my_answer = ""
language = ""
counter = 0
p = 0
screen = ""


# ------CLASSES

class SplashScreen(QSplashScreen):  # first window
    def __init__(self):
        super(SplashScreen, self).__init__()
        uic.loadUi('screens/splashscreen.ui', self)

        self.setWindowFlag(Qt.FramelessWindowHint)  # Removes the frame of the window
        # self.showMaximized()  # opening window in maximized size

    def thread(self):
        t1 = Thread(target=self.Operation)
        t1.start()

    def Operation(self):
        print("time start")
        time.sleep(10)
        print("time stop")

    def progress(self):
        # speak("Welcome button clicked")
        for i in range(100):
            sleep(0.001)
            self.progressBar.setValue(i)


def thread(self, target="self.Operation"):
    print("Thread started")
    t1 = Thread(target=target)
    t1.start()


class MainPage(QDialog):  # first window
    def __init__(self):
        super(MainPage, self).__init__()
        uic.loadUi('screens/welcome.ui', self)
        self.btnTopics.clicked.connect(thread)
        self.btnQuiz.clicked.connect(self.showQuiz)
        self.btnTranslate.clicked.connect(self.showTranslate)
        self.btnAbout.clicked.connect(self.showAbout)

        # Add Push Button
        clear_btn = QPushButton('Click Me', self)
        clear_btn.clicked.connect(self.thread)

        # self.showMaximized()  # opening window in maximized size
        snr.speak("Goodmorning Learner!")
        # # changing the text of label
        # self.Title_2.setText("Goodmorning learner")

    def Operation(self):
        print("time start")
        time.sleep(10)
        print("time stop")

    def showTopics(self):
        snr.speak("Topics")
        self.lesson = topics()
        self.lesson.show()
        self.hide()

    def showQuiz(self):
        snr.speak("Quiz")
        self.lesson = quiz()
        self.lesson.show()
        self.hide()

    def showTranslate(self):
        snr.speak("Translate")
        self.activity = translate()
        self.activity.show()
        self.hide()

    def showAbout(self):
        snr.speak("About Me")
        self.activity = about()
        self.activity.show()
        self.hide()

    # self.welcome = Form()
    # self.welcome.show()
    # self.hide()


class topics(QDialog):  # second screen showing the lesson and activity
    def __init__(self):
        super(topics, self).__init__()
        uic.loadUi('screens/topics.ui', self)
        snr.speak(
            "Let us learn something new! You can choose between rhyming words, short stories, and polite expressions. Which one should we try? ")
        self.showMaximized()  # opening window in maximized size


class Menu(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super(Menu, self).__init__()
        uic.loadUi('second.ui', self)
        self.btn3.clicked.connect(self.show_lesson)
        self.btn4.clicked.connect(self.show_activity)
        # snr.speak("Try saying. i want to learn. or. i want to play")

    def show_lesson(self):
        snr.speak("You choose to learn!")
        self.lesson = window1()
        self.lesson.show()
        self.hide()

    def show_activity(self):
        snr.speak("You choose to challenge. nice!")
        self.activity = Activity()
        self.activity.show()
        self.hide()


class window1(QWidget):
    def __init__(self):
        global language, counter
        super().__init__()
        uic.loadUi('window1.ui', self)
        self.TIMER = QTimer(self)
        self.TIMER.start(0)
        snr.speak("Lesson")

        # video recorder
        self.btn_hide.clicked.connect(self.ask_ettibot)
        self.btn3.clicked.connect(self.show_activity)
        language = "en"
        mytext = "Hello, my name is ettibot. I am your english teacher."
        self.txt_ettibot_words.append("ettibot: " + mytext)
        snr.speak(mytext)

    def show_activity(self):
        self.activity = Activity()
        self.activity.show()
        self.hide()


class Activity(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('activity.ui', self)
        snr.speak("Activity")
        self.start.clicked.connect(self.show_Quiz1)

    def show_Quiz1(self):
        self.quiz = quiz1()
        self.quiz.show()
        self.hide()
        snr.speak("Start")


class quiz(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Quizzes.ui', self)
        snr.speak("Quiz. number. one")
        self.my_countdown_timer = QTimer()

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
        
        


# ------FUNCTIONS

# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    print("Speak Now . . .")

    r = sr.Recognizer()
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False

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
            return "topics"

    return text


# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    global my_answer, counter, user_input, respond
    counter += 1
    # Call LED lights here
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    os.remove(filename)  # remove temporary file
    

def my_loop():
    while True:
        query = snr.ask_ettibot().lower()
        # translator
        if any(i in query for i in ["translate", "tagalog ng", "english ng"]):
            word = query.replace(["translate", "tagalog ng", "english ng"], '')

            print(word)
            detected_lang = translator.detect(word)
            print(detected_lang.lang)

            if detected_lang.lang == 'en':
                translate_text = translator.translate(word, dest='tl')
                print(translate_text)
                speak(translate_text.text, 'tl')

            elif detected_lang.lang == 'tl':
                translate_text = translator.translate(word, dest='en')
                print(translate_text)
                speak(translate_text.text, 'en')

        # topics
        elif any(i in query for i in ["topics", "show topics", "what's the lessons"]):
            window = Window()
            window.runTasks2()

        # quiz
        elif any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
            window = MainPage()
            window.showQuiz()


        # about me
        elif "about" in query:
            window.showAbout()

        elif "none" in query:
            print(query)

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
            
# 1. Subclass QRunnable
class Runnable(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.n = n
        speak("this is runnable subclass")

    def run(self):
        # Your long-running task goes here ...
        for i in range(5):
           logging.info(f"Working in thread {self.n}, step {i + 1}/5")
           time.sleep(random.randint(700, 2500) / 1000)
           
              
class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('MainWindow.ui', self)
        #self.setupUi()
        self.showMaximized()  # opening window in maximized size
        
        # Create and connect widgets
        self.btnTopics.clicked.connect(self.runTopics)
        self.btnQuiz.clicked.connect(self.runQuiz)
        self.btnTranslate.clicked.connect(self.runTranslate)
        self.btnAbout.clicked.connect(self.runAbout)
        
    def runTopics(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText("Topics")
        speak("You have selected Topics")
        
    def runQuiz(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText("Topics")
        speak("You have selected Quiz")
        
    def runTranslate(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText("Topics")
        speak("You have selected Translate")
        
    def runAbout(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText("Topics")
        speak("You have selected About")

    def setupUi(self):
        self.setWindowTitle("QThreadPool + QRunnable")
        self.resize(250, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        # Create and connect widgets
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        countBtn = QPushButton("Click me!")
        countBtn.clicked.connect(self.runTasks)

        countBtn2 = QPushButton("Say Hello")
        countBtn2.clicked.connect(self.runTasks2)
        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(countBtn)
        layout.addWidget(countBtn2)
        self.centralWidget.setLayout(layout)
        speak("setup you I")
        
    def runTasks2(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText("Hello!")
        speak("Hello")

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        for i in range(threadCount):
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(i)
            # 3. Call start()
            pool.start(runnable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = Window()
    #window.show()
    speak("You can say the word to select.")
    
    #start threading
    t = threading.Thread(target=my_loop)
    t.setDaemon(True)
    t.start()
    
    window = Window()
    window.show()
    sys.exit(app.exec())
