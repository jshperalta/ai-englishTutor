import sys

from PySide2.QtCore import QObject, QTimer, Signal
from PySide2.QtWidgets import QApplication, QMainWindow


class Producer(QObject):
    letterChanged = Signal(str)

    def __init__(self, parent=None):
        super(Producer, self).__init__(parent)

        self._text = ""
        self._text_it = None
        self._timer = QTimer(self, timeout=self._handle_timeout)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def start(self, interval=1000):
        self._text_it = iter(self.text)
        self._timer.start(interval)
        self._handle_timeout()

    def stop(self):
        self._timer.stop()
        self._text_it = None

    def _handle_timeout(self):
        try:
            letter = next(self._text_it)
        except StopIteration as e:
            self._timer.stop()
        else:
            self.letterChanged.emit(letter)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mensaje = Ui_MainWindow()
        self.mensaje.setupUi(self)

        self.producer = Producer()
        self.producer.text = "hello world"

        self.producer.letterChanged.connect(self.mensaje.texto.insert)
        self.mensaje.pushButton_2.clicked.connect(self.handle_clicked)

    def handle_clicked(self):
        self.producer.start(500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

# from PyQt5.QtWidgets import *
# from PyQt5 import QtCore
# from PyQt5.QtGui import *
# import sys
#
#
# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # informations
#         info = "info"
#         new_info = "how to"
#
#         # set the title
#         self.setWindowTitle("Label")
#
#         # setting  the geometry of window
#         self.setGeometry(0, 0, 1024, 600)
#
#         # creating a label widget
#         self.label_1 = QLabel(info, self)
#
#         # moving position
#         self.label_1.move(100, 100)
#
#         # setting up border
#         self.label_1.setStyleSheet("border: 1px solid black; font-size: 36px;")
#
#         # creating a label widget
#         self.label_2 = QLabel(info, self)
#
#         # moving position
#         self.label_2.move(100, 150)
#
#         # setting up border
#         self.label_2.setStyleSheet("border: 1px solid black;")
#
#         # changing the text of label
#         self.label_2.setText(new_info)
#
#         # adjusting the size of label
#         self.label_1.adjustSize()
#
#         # adjusting the size of label
#         self.label_2.adjustSize()
#
#         # show all the widgets
#         self.show()
#
#
# # create pyqt5 app
# App = QApplication(sys.argv)
#
# # create the instance of our Window
# window = Window()
#
# # start the app
# sys.exit(App.exec())
