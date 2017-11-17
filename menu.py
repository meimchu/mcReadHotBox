# Created by: Mei Chu
# Last updated: November 16, 2017

import mcReadHotBox
import nuke

nuke.menu("Nodes").addCommand('mcTools/mcReadHotBox', 'mcReadHotBoxActivate()', 'z')

def mcReadHotBoxActivate():
    reload(mcReadHotBox)
    mcReadHotBox.main()