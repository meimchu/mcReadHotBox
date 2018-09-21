# Created by: Mei Chu
# Last updated: September 20, 2018
# Version: 0.1.3

import nuke
import subprocess
import re

try:
    from PySide.QtGui import *
    from PySide.QtCore import *

except Exception:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *

# Global variable for the size of the labels and search box inside the panel
fixed_width = 150
fixed_height = 30


def set_default_colour(hotbox, search_box):
    if search_box.text() in hotbox.text():
        hotbox.setStyleSheet('background:rgb(60, 60, 60);color:white')

    else:
        hotbox.setStyleSheet('background:transparent;color:gray')


class Panel(QDialog):
    def __init__(self, hotbox_count, col_count, row_count):
        super(Panel, self).__init__()

        # Bring in global variables as needed
        self.hotbox_count = hotbox_count
        self.col_count = col_count
        self.row_count = row_count

        # Set the look of panel
        self.setObjectName('widget_panel')
        self.layout = QGridLayout()
        self.layout.setVerticalSpacing(5)
        self.setWindowFlags(Qt.Popup)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # Add search box at the start
        self.search_box = SearchBox(self)
        self.layout.addWidget(self.search_box, 0, 0)

        # Set variable for the selected node
        self.mc_read = nuke.selectedNode()

        # Determine the amount of channels available at selected node
        self.read_data = []
        for channel in self.mc_read.channels():
            main_channel = channel.split('.')[0]
            if main_channel not in self.read_data:
                self.read_data.append(main_channel)

        self.mc_read_length = len(self.read_data)

        # Counting the channels and adding it as a label widget
        while self.hotbox_count < self.mc_read_length:
            self.hotbox_name = self.read_data[self.hotbox_count]

            rgba_list = ['rgba.red', 'rgba.green', 'rgba.blue', 'rgba.alpha']

            self.label = ActionLabel(self.hotbox_name, self, self.search_box)
            if self.hotbox_name in rgba_list:
                self.layout.addWidget(self.label, self.row_count, 0)

            else:
                # Every time 10 hot boxes appear, move to the next column
                if (self.hotbox_count + 1) % 10 == 0:
                    self.col_count += 1
                    self.row_count = 0

                self.layout.addWidget(self.label, self.row_count, self.col_count)

            self.hotbox_count += 1
            self.row_count += 1

        self.setLayout(self.layout)

        # Functions that will move the panel around based on cursor position
        self.monitor_res = self.get_resolution()
        self.cursor_position = self.get_mouse_position()
        self.move_panel()

        # Set search box as the main focus
        self.search_box.setFocus()

    def get_mouse_position(self):
        # Move panel to beside current mouse position
        x_pos = QCursor.pos().x()
        y_pos = QCursor.pos().y()
        return tuple([x_pos, y_pos])
        # self.move(self.cursor_position - QPoint(5, 5))

    def get_resolution(self):
        results = str(subprocess.Popen(['system_profiler SPDisplaysDataType'], stdout=subprocess.PIPE, shell=True).communicate()[0])
        res = re.search('Resolution: \d* x \d*', results).group(0).split(' ')
        width, height = int(res[1]) / 2, int(res[3]) / 2

        return tuple([width, height])

    def move_panel(self):
        x_cursor = self.cursor_position[0]
        y_cursor = self.cursor_position[1]
        x_monitor = self.monitor_res[0]
        y_monitor = self.monitor_res[1]

        if self.col_count == 0:
            y_panel_size = int(self.row_count * fixed_height)

        else:
            y_panel_size = int(10 * fixed_height)

        x_panel_size = (self.col_count + 1) * fixed_width

        # Move panel if cursor's Y position plus panel size goes off the edge
        if (y_cursor + y_panel_size) > y_monitor:
            y_pos = y_cursor - y_panel_size

        else:
            y_pos = y_cursor

        # Move panel if cursor's X position plus panel size goes off the edge
        if (x_cursor + x_panel_size) > x_monitor:
            x_pos = x_cursor - x_panel_size

        else:
            x_pos = x_cursor

        self.move(QPoint(x_pos, y_pos))


class ActionLabel(QLabel):
    def __init__(self, hotbox_name, panel, search_box):
        super(ActionLabel, self).__init__()

        # Bring in global variable as needed
        self.hotbox_name = hotbox_name
        self.panel = panel
        self.search_box = search_box

        # Set the look of label
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(fixed_width)
        self.setFixedHeight(fixed_height)

        # Set variables for the selected node
        self.mc_read = nuke.selectedNode()

        # Set text to the label
        self.setText(self.hotbox_name)
        self.setObjectName(self.hotbox_name)
        self.default_colour()

    def default_colour(self):
        # Set default label scheme for rgb
        set_default_colour(self, self.search_box)

    def enterEvent(self, event):
        # Set colour of label when selected
        self.setStyleSheet('background:orange;color:white')

    def leaveEvent(self, event):
        # Set colour of label back to default scheme
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

        # Bring in global variables as needed
        self.panel = panel

        # Set the look of the line edit
        self.setObjectName('search_box')
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(fixed_width)
        self.setFixedHeight(fixed_height)
        self.setText('')

        # Set text change signal
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
