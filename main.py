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

import sys
import defines.speakandrecognize as snr

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic import *

translator = Translator()

my_answer = ""
language = ""
counter = 0
p = 0
screen = ""


# ------CLASSES

class SplashScreen(QSplashScreen):  # first window
    def __init__(self):
        super(QSplashScreen, self).__init__()
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


class MainPage(QDialog):  # first window
    def __init__(self):
        super(MainPage, self).__init__()
        uic.loadUi('screens/welcome.ui', self)
        self.btnTopics.clicked.connect(thread, showTopics)
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

    def thread(self, target="self.Operation"):
        t1 = Thread(target=target)
        t1.start()

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

def my_loop(queue):
    while MainPage:
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
                snr.speak(translate_text.text, 'tl')

            elif detected_lang.lang == 'tl':
                translate_text = translator.translate(word, dest='en')
                print(translate_text)
                snr.speak(translate_text.text, 'en')

        # topics
        if any(i in query for i in ["topics", "show topics", "what's the lessons"]):
            window = MainPage()
            window.showTopics()

        # quiz
        if any(i in query for i in ["quiz", "show quiz", "what's the challenge"]):
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
            snr.speak(res)

        # respond politely
        elif any(i in query for i in ["hi", "hello", "can you hear me"]):
            res = np.random.choice(
                ["hi", "hello!", "yes?", "I can hear you", "What do you need?"])
            snr.speak(res)

        else:
            snr.speak("Sorry, I don't understand what you said. Please try again.")
            print(query)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    snr.speak("Please wait. while I'm initiating myself")
    splash.progress()
    snr.speak("Done!")
    window = MainPage()
    window.show()

    splash.finish(window)

    try:
        sys.exit(APP.exec_())

    except SystemExit:
        print()
