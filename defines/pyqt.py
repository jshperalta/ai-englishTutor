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

import sys
import defines.speakandrecognize as snr

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic import *

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from PyQt5 import QtCore, QtGui, QtWidgets

logging.basicConfig(format="%(message)s", level=logging.INFO)


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


# 1. Subclass QRunnable
class Runnable(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        # Your long-running task goes here ...
        snr.speak("logging")
        for i in range(5):
            logging.info(f"Working in thread {self.n}, step {i + 1}/5")
            time.sleep(random.randint(700, 2500) / 1000)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

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
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(countBtn)
        self.centralWidget.setLayout(layout)
        snr.speak("setup u.i")

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        snr.speak("pool")
        for i in range(threadCount):
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(i)
            # 3. Call start()
            pool.start(runnable)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
