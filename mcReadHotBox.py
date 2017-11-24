# Created by: Mei Chu
# Last updated: November 23, 2017

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

# Global variables
hotbox_count = 0
col_count = 1
row_count = 0

class Panel(QDialog):
    def __init__(self):
        super(Panel, self).__init__()

        # Setting the look of panel
        self.layout = QGridLayout()
        mouse_position = QCursor.pos()
        self.move(mouse_position - QPoint(100, 100))
        self.resize(150, 30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.setVerticalSpacing(5)
        self.setAttribute(Qt.WA_QuitOnClose)

        # Adding searchbox at the start
        self.layout.addWidget(Searchbox(), 0, 0)

        # Bring in global variables as needed
        global hotbox_count
        global col_count
        global row_count

        # Setting variable for the selected node
        mcRead = nuke.selectedNode()

        # Determining the amount of channels available at selected node
        mcReadLength = len(mcRead.channels())

        # Counting the channels and adding it as a label widget
        while hotbox_count < mcReadLength:
            mcReadData = mcRead.channels()
            hotbox_name = mcReadData[hotbox_count]

            if hotbox_name == "rgba.red":
                self.layout.addWidget(ActionLabel(), hotbox_count + 1, 0)

            elif hotbox_name == "rgba.green":
                self.layout.addWidget(ActionLabel(), hotbox_count + 1, 0)

            elif hotbox_name == "rgba.blue":
                self.layout.addWidget(ActionLabel(), hotbox_count + 1, 0)

            elif hotbox_name == "rgba.alpha":
                self.layout.addWidget(ActionLabel(), hotbox_count + 1, 0)

            else:
                self.layout.addWidget(ActionLabel(), row_count, col_count)
                row_count += 1
                if (hotbox_count + 2) % 5 == 0:
                    col_count += 1
                    row_count = 0
            hotbox_count += 1

        self.setLayout(self.layout)

class ActionLabel(QLabel):
    def __init__(self):
        super(ActionLabel, self).__init__()

        # Setting the look of label
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(150)
        self.setFixedHeight(30)
        self.setStyleSheet("background:grey;color:white")

        # Bring in global variable as needed
        global hotbox_count

        # Setting variables for the selected node
        mcRead = nuke.selectedNode()
        mcReadData = mcRead.channels()
        hotbox_name = mcReadData[hotbox_count]

        # Setting text to the label
        self.setText(hotbox_name)
        self.setObjectName(hotbox_name)

        # Setting default label scheme for rgb
        if hotbox_name == "rgba.red":
            self.setStyleSheet("background:red;color:white")

        elif hotbox_name == "rgba.green":
            self.setStyleSheet("background:green;color:white")

        elif hotbox_name == "rgba.blue":
            self.setStyleSheet("background:blue;color:white")

    def enterEvent(self, event):

        # Setting colour of label when selected
        self.setStyleSheet('background:orange;color:white')

    def leaveEvent(self, event):

        # Setting colour of label back to default scheme
        self.setStyleSheet('background:grey;color:white')
        if self.text() == "rgba.red":
            self.setStyleSheet("background:red;color:white")

        elif self.text() == "rgba.green":
            self.setStyleSheet("background:green;color:white")

        elif self.text() == "rgba.blue":
            self.setStyleSheet("background:blue;color:white")

    def mousePressEvent(self, event):
        print "Clicked on", self.text()
        viewer = nuke.activeViewer().node()['channels']
        viewer.setValue(self.text())

class Searchbox(QLineEdit):
    def __init__(self):
        super(Searchbox, self).__init__()

        # Setting the look of the line edit
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(150)
        self.setFixedHeight(30)

def main():
    panel = Panel()
    panel.exec_()