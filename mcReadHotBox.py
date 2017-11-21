# Created by: Mei Chu
# Last updated: November 19, 2017

try:
    from PySide.QtGui import *
except:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *

try:
    from PySide.QtCore import *
except:
    from PySide2.QtCore import *

import nuke

hotbox_count = 0
col_count = 1
row_count = 0

class Panel(QDialog):
    def __init__(self):
        super(Panel, self).__init__()
        self.layout = QGridLayout()
        mouse_position = QCursor.pos()
        self.move(mouse_position - QPoint(100, 100))
        self.resize(150, 30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.setVerticalSpacing(5)
        self.setAttribute(Qt.WA_QuitOnClose)
        self.setMouseTracking(True)

        global hotbox_count
        global col_count
        global row_count

        mcRead = nuke.selectedNode()
        mcReadLength = len(mcRead.channels())
        while hotbox_count < mcReadLength:
            mcReadData = mcRead.channels()
            if mcReadData[hotbox_count] == "rgba.red":
                self.layout.addWidget(ActionLabel(), hotbox_count, 0)

            elif mcReadData[hotbox_count] == "rgba.green":
                self.layout.addWidget(ActionLabel(), hotbox_count, 0)

            elif mcReadData[hotbox_count] == "rgba.blue":
                self.layout.addWidget(ActionLabel(), hotbox_count, 0)

            elif mcReadData[hotbox_count] == "rgba.alpha":
                self.layout.addWidget(ActionLabel(), hotbox_count, 0)

            else:
                self.layout.addWidget(ActionLabel(), row_count, col_count)
                row_count += 1
                if (hotbox_count + 1) % 4 == 0:
                    col_count += 1
                    row_count = 0
            hotbox_count += 1

        self.layout.addWidget(QLabel())
        self.setLayout(self.layout)

class ActionLabel(QLabel):
    def __init__(self):
        super(ActionLabel, self).__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(150)
        self.setFixedHeight(30)
        self.setStyleSheet("background:grey;color:white")
        global hotbox_count

        mcRead = nuke.selectedNode()
        mcReadData = mcRead.channels()
        hotbox_name = mcReadData[hotbox_count]
        self.setText(hotbox_name)
        self.setObjectName(hotbox_name)
        if mcReadData[hotbox_count] == "rgba.red":
            self.setStyleSheet("background:red;color:white")

        elif mcReadData[hotbox_count] == "rgba.green":
            self.setStyleSheet("background:green;color:white")

        elif mcReadData[hotbox_count] == "rgba.blue":
            self.setStyleSheet("background:blue;color:white")

    def enterEvent(self, event):

        self.setStyleSheet('background:orange;color:white')

    def leaveEvent(self, event):

        self.setStyleSheet('background:grey;color:white')
        if self.text() == "rgba.red":
            self.setStyleSheet("background:red;color:white")

        elif self.text() == "rgba.green":
            self.setStyleSheet("background:green;color:white")

        elif self.text() == "rgba.blue":
            self.setStyleSheet("background:blue;color:white")

def main():
    panel = Panel()
    panel.exec_()