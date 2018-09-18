# Created by: Mei Chu
# Last updated: September 17, 2018
# Version: 0.1.1

import nuke

try:
    from PySide.QtGui import *
    from PySide.QtCore import *

except Exception:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *


def set_default_colour(hotbox, search_box):
    if search_box.text() in hotbox.text():
        hotbox.setStyleSheet('background:rgb(70, 70, 70);color:white')

        if hotbox.text() == "rgba.red":
            hotbox.setStyleSheet("background:red;color:white")

        elif hotbox.text() == "rgba.green":
            hotbox.setStyleSheet("background:green;color:white")

        elif hotbox.text() == "rgba.blue":
            hotbox.setStyleSheet("background:blue;color:white")

    else:
        hotbox.setStyleSheet('background:transparent;color:gray')


class Panel(QDialog):
    def __init__(self, hotbox_count, col_count, row_count):
        super(Panel, self).__init__()

        # Setting the look of panel
        self.setObjectName('widget_panel')
        self.layout = QGridLayout()
        self.layout.setVerticalSpacing(5)
        self.resize(150, 30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_QuitOnClose)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # Move panel to beside current mouse position
        self.mouse_position = QCursor.pos()
        self.move(self.mouse_position)

        # Adding searchbox at the start
        self.search_box = SearchBox(self)
        self.layout.addWidget(self.search_box, 0, 0)

        # Bring in global variables as needed
        self.hotbox_count = hotbox_count
        self.col_count = col_count
        self.row_count = row_count

        # Setting variable for the selected node
        mc_read = nuke.selectedNode()

        # Determining the amount of channels available at selected node
        mc_read_length = len(mc_read.channels())

        # Counting the channels and adding it as a label widget
        while self.hotbox_count < mc_read_length:
            read_data = mc_read.channels()
            hotbox_name = read_data[self.hotbox_count]

            rgba_list = ['rgba.red', 'rgba.green', 'rgba.blue', 'rgba.alpha']

            if hotbox_name in rgba_list:
                self.layout.addWidget(ActionLabel(self.hotbox_count, self, self.search_box), self.row_count, 0)

            else:
                # Every time 6 hot boxes appear, move to the next column
                if (self.hotbox_count + 1) % 10 == 0:
                    self.col_count += 1
                    self.row_count = 0

                self.layout.addWidget(ActionLabel(self.hotbox_count, self, self.search_box), self.row_count, self.col_count)

            self.hotbox_count += 1
            self.row_count += 1

        self.setLayout(self.layout)


class ActionLabel(QLabel):
    def __init__(self, hotbox_count, panel, search_box):
        super(ActionLabel, self).__init__()

        # Setting the look of label
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(150)
        self.setFixedHeight(30)

        # Bring in global variable as needed
        self.hotbox_count = hotbox_count
        self.panel = panel
        self.search_box = search_box

        # Setting variables for the selected node
        self.mc_read = nuke.selectedNode()
        self.read_data = self.mc_read.channels()
        self.hotbox_name = self.read_data[self.hotbox_count]

        # Setting text to the label
        self.setText(self.hotbox_name)
        self.setObjectName(self.hotbox_name)
        self.default_colour()

    def default_colour(self):
        # Setting default label scheme for rgb
        set_default_colour(self, self.search_box)

    def enterEvent(self, event):
        # Setting colour of label when selected
        self.setStyleSheet('background:orange;color:white')

    def leaveEvent(self, event):
        # Setting colour of label back to default scheme
        self.default_colour()

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ShiftModifier:
            shuffle_node = nuke.nodes.Shuffle(label=self.hotbox_name, inputs=[self.mc_read])
            shuffle_node['in'].setValue(self.hotbox_name)

        elif modifiers == Qt.ControlModifier:
            grade_node = nuke.nodes.Grade(label=self.hotbox_name, inputs=[self.mc_read])
            grade_node['channels'].setValue(self.hotbox_name)

        else:
            try:
                viewer = nuke.activeViewer().node()['channels']
                viewer.setValue(self.text())

            except Exception:
                pass

        self.panel.close()


class SearchBox(QLineEdit):
    def __init__(self, panel):
        super(SearchBox, self).__init__()

        self.panel = panel

        # Setting the look of the line edit
        self.setObjectName('search_box')
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(150)
        self.setFixedHeight(30)
        self.textChanged.connect(self.text_changed)

        try:
            self.setPlaceholderText('Search...')

        except Exception:
            pass

    def text_changed(self):
        for index in range(self.panel.layout.count()):
            name = self.panel.layout.itemAt(index).widget().objectName()
            selected_label = self.panel.layout.itemAt(index).widget()

            if self.text() != '':
                self.change_colour(name, selected_label)

            else:
                self.change_colour(name, selected_label)

            # Using this would hide/show the buttons instead
            # if self.text() not in name and 'search_box' not in name:
            #     self.panel.layout.itemAt(index).widget().hide()
            #
            # else:
            #     self.panel.layout.itemAt(index).widget().show()

    def change_colour(self, name, selected_label):
        if self.text() in name and 'search_box' not in name:
            set_default_colour(selected_label, self)

        elif 'search_box' in name:
            selected_label.setStyleSheet('')

        else:
            selected_label.setStyleSheet('background:transparent;color:gray')


def load_hotbox():
    # Only show one the panel if one node is selected
    if len(nuke.selectedNodes()) == 1:
        # Global variables at start
        hotbox_count = 0
        col_count = 0
        row_count = 1

        panel = Panel(hotbox_count, col_count, row_count)
        panel.exec_()
