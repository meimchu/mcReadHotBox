# Created by: Mei Chu
# Last updated: October 23, 2018

import nuke

nuke.menu("Nodes").addCommand('mcTools/mcReadHotBox', 'mcReadHotBoxActivate()', 'z')


def mcReadHotBoxActivate():
    import mcReadHotBox
    mcReadHotBox.load_hotbox()
