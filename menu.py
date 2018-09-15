# Created by: Mei Chu
# Last updated: September 15, 2018

import mcReadHotBox
import nuke

nuke.menu("Nodes").addCommand('mcTools/mcReadHotBox', 'mcReadHotBoxActivate()', 'z')


def mcReadHotBoxActivate():
    mcReadHotBox.load_hotbox()
