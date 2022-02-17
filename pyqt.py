from PySide.QtGui import QApplication, QProgressBar, QWidget
from PySide.QtCore import QTimer
import time

app = QApplication([])
pbar = QProgressBar()
pbar.setMinimum(0)
pbar.setMaximum(100)

pbar.show()

animation = QPropertyAnimation(pbar, "value")
animation.setDuration(2000)
animation.setStartValue(0)
animation.setEndValue(100)
animation.start()

app.exec_()

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
