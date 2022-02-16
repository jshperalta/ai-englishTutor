# MAIN CODE
import os
import pyglet
from gtts import gTTS
import pygame
import speech_recognition as sr
import sys
import cv2
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

my_answer = ""
language = ""
counter = 0
user_input = ['hi', 'hello', 'good morning', 'good afternoon', 'good evening', 'what is lesson for today',
              'lesson for today', 'whats the lesson, ettibot']

respond = ['hello', 'hi', 'good morning too', 'good afternoon too', 'good evening too']

# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    global my_answer, counter, user_input, respond
    counter += 1
    print("Speak Now . . .")
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)
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


def speak(text, lang="en"):  # here audio is var which contain text
    # Call LED lights here
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    sleep(music.duration)  # prevent from killing
    os.remove(filename)  # remove temporary file


class win(QWidget):  # first window
    def __init__(self):
        super().__init__()
        uic.loadUi('welcome.ui', self)
        self.btn1.clicked.connect(self.show_welcome)
        speak("Goodmorning Learner!")

    def show_welcome(self):
        # speak("Welcome button clicked")
        self.welcome = Form()
        self.welcome.show()
        self.hide()


class Form(QWidget):  # second screen showing the lesson and activity
    def __init__(self):
        super().__init__()
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

    # def show_Quiz1(self):
    #     self.quiz = quiz1()
    #     self.quiz.show()
    #     self.hide()
    #     speak("Start")


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
        super(). __init__()
        uic.loadUi('Q2,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz3()
        self.next.show()
        self.hide()

class quiz3(QWidget):
    def __init__(self):
        super(). __init__()
        uic.loadUi('Q3,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz4()
        self.next.show()
        self.hide()

class quiz4(QWidget):
    def __init__(self):
        super(). __init__()
        uic.loadUi('Q4,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz5()
        self.next.show()
        self.hide()

class quiz5(QWidget):
    def __init__(self):
        super(). __init__()
        uic.loadUi('Q5,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = quiz6()
        self.next.show()
        self.hide()

class quiz6(QWidget):
    def __init__(self):
        super(). __init__()
        uic.loadUi('Q6,ui', self)
        self.pushButton.clicked.connect(self.show)

    def show_next(self):
        self.next = QPushButton()
        self.next.show()
        self.hide()


if __name__ == '__main__':

    APP = QApplication(sys.argv)
    MY_APP = win()
    MY_APP.show()

    try:
        sys.exit(APP.exec_())

    except SystemExit:
        print()