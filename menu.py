# Created by: Mei Chu
# Last updated: September 15, 2018

import nuke

nuke.menu("Nodes").addCommand('mcTools/mcReadHotBox', 'mcReadHotBoxActivate()', 'z')


def mcReadHotBoxActivate():
    import mcReadHotBox
    mcReadHotBox.load_hotbox()
