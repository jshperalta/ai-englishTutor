# MAIN CODE
import os
import time
import datetime
import numpy as np
import pyglet
from gtts import gTTS
import pygame
import speech_recognition as sr
import sys

from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic import *

my_answer = ""
language = ""
counter = 0
p = 0
user_input = ['hi', 'hello', 'good morning', 'good afternoon', 'good evening', 'what is lesson for today',
              'lesson for today', 'whats the lesson, ettibot']

respond = ['hello', 'hi', 'good morning too', 'good afternoon too', 'good evening too']


# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    global my_answer, counter, user_input, respond
    counter += 1
    print("Speak Now . . .")

    r = sr.Recognizer()
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False

    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source, phrase_time_limit=10)
        # Call LED lights here

        try:
            # Call LED lights here
            print("Recognising....")
            text = r.recognize_google(audio, language='en')
            print(text)

        except Exception as e:
            print("Exception " + str(e))
            return "none"

    return text


# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    # Call LED lights here
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    sleep(music.duration)  # prevent from killing
    os.remove(filename)  # remove temporary file


class SplashScreen(QSplashScreen):  # first window
    def __init__(self):
        super(QSplashScreen, self).__init__()
        uic.loadUi('splashscreen.ui', self)

        self.setWindowFlag(Qt.FramelessWindowHint)  # Removes the frame of the window
        self.showMaximized()  # opening window in maximized size
        # speak("Goodmorning Learner!")

    def progress(self):
        # speak("Welcome button clicked")
        for i in range(100):
            sleep(0.01)
            self.progressBar.setValue(i)


class MainPage(QDialog):  # first window
    def __init__(self):
        super(MainPage, self).__init__()
        uic.loadUi('welcome.ui', self)
        self.btnTopics.clicked.connect(self.showTopics)
        self.btnQuiz.clicked.connect(self.showQuiz)
        self.btnTranslate.clicked.connect(self.showTranslate)
        self.btnAbout.clicked.connect(self.showAbout)
        self.showMaximized()  # opening window in maximized size
        speak("Goodmorning Learner!")
        # # changing the text of label
        # self.Title_2.setText("Goodmorning learner")

    def showTopics(self):
        speak("Topics")
        self.lesson = topics()
        self.lesson.show()
        self.hide()

    def showQuiz(self):
        speak("Quiz")
        self.lesson = window1()
        self.lesson.show()
        self.hide()

    def showTranslate(self):
        speak("Translate")
        self.activity = Activity()
        self.activity.show()
        self.hide()

    def showAbout(self):
        speak("About Me")
        self.activity = Activity()
        self.activity.show()
        self.hide()

    # self.welcome = Form()
    # self.welcome.show()
    # self.hide()


class topics(QDialog):  # second screen showing the lesson and activity
    def __init__(self):
        super(topics, self).__init__()
        uic.loadUi('topics.ui', self)

        # speak("Try saying. i want to learn. or. i want to play")


class Menu(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super(Menu, self).__init__()
        uic.loadUi('second.ui', self)
        self.btn3.clicked.connect(self.show_lesson)
        self.btn4.clicked.connect(self.show_activity)
        # speak("Try saying. i want to learn. or. i want to play")

    def show_lesson(self):
        speak("You choose to learn!")
        self.lesson = window1()
        self.lesson.show()
        self.hide()

    def show_activity(self):
        speak("You choose to challenge. nice!")
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
        speak("Lesson")

        # video recorder
        self.btn_hide.clicked.connect(self.ask_ettibot)
        self.btn3.clicked.connect(self.show_activity)
        language = "en"
        mytext = "Hello, my name is ettibot. I am your english teacher."
        self.txt_ettibot_words.append("ettibot: " + mytext)
        speak(mytext)

    def show_activity(self):
        self.activity = Activity()
        self.activity.show()
        self.hide()


class Activity(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('activity.ui', self)
        speak("Activity")
        self.start.clicked.connect(self.show_Quiz1)

    def show_Quiz1(self):
        self.quiz = quiz1()
        self.quiz.show()
        self.hide()
        speak("Start")


class quiz1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Q1.ui', self)
        speak("Quiz. number. one")
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

    def show_Quiz2(self):
        self.my_countdown_timer.stop()
        self.quiz = quiz2()
        self.quiz.show()
        self.hide()
        speak("Quiz number 2")


class quiz2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Q2,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz3()
        self.next.show()
        self.hide()


class quiz3(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Q3,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz4()
        self.next.show()
        self.hide()


class quiz4(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Q4,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz5()
        self.next.show()
        self.hide()


class quiz5(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Q5,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz6()
        self.next.show()
        self.hide()


class quiz6(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Q6,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = QPushButton()
        self.next.show()
        self.hide()


if __name__ == '__main__':

    APP = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    speak("Please wait. while I'm initiating myself")
    splash.progress()
    speak("Done!")

    window = MainPage()
    window.show()

    splash.finish(window)

    while (True):
        query = ask_ettibot().lower()
        # wake up
        if "topics" in query:
            window = MainPage()
            window.showTopics()

        # action time
        elif "quiz" in query:
            window = MainPage()
            window.showQuiz()

        # action time
        elif "translate" in query:
            window.showTranslate()

        # action tim
        elif "about" in query:
            window.showAbout()

        else:
            speak("Sorry, I don't understand what you said. Please try again.")

    # while True:
    #     query = ask_ettibot().lower()
    #
    #     ## wake up
    #     if ask_ettibot() is True:
    #         res = "Hello I am Athena the Teacher, what can I do for you?"
    #
    #     ## action time
    #     elif "time" in query:
    #         res = ai.action_time()
    #
    #     ## respond politely
    #     elif any(i in query for i in ["thank", "thanks"]):
    #         res = np.random.choice(
    #             ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "peace out!"])

    ## conversation
    # else:
    #     chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
    #     res = str(chat)
    #     res = res[res.find("bot >> ") + 6:].strip()
    # ai.text_to_speech(res)

    try:
        sys.exit(APP.exec_())

    except SystemExit:
        print()
