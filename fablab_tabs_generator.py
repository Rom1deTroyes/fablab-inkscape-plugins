#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *
import simplepath

from fablab_box_lib import BoxEffect
from fablab_lib import BaseEffect


def print_(*arg):
    f = open("fablab_debug.log", "a")
    for s in arg:
        s = str(unicode(s).encode('unicode_escape')) + " "
        f.write(s)
    f.write("\n")
    f.close()


def unsignedLong(signedLongString):
    longColor = long(signedLongString)
    if longColor < 0:
        longColor = longColor & 0xFFFFFFFF
    return longColor


def getColorString(longColor):

    longColor = unsignedLong(longColor)
    hexColor = hex(longColor)[2:-3]
    hexColor = hexColor.rjust(6, '0')
    return '#' + hexColor.upper()


class BoxGeneratorEffect(BaseEffect, BoxEffect):

    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        BaseEffect.__init__(self)

        self.OptionParser.add_option('-i', '--path_id', action='store',
                                     type='string', dest='path_id', default='encoches',
                                     help='Id of svg path')

        self.OptionParser.add_option('--width', action='store',
                                     type='float', dest='width', default=200,
                                     help='Width')

        self.OptionParser.add_option('--thickness', action='store',
                                     type='float', dest='thickness', default=3,
                                     help='Thickness of material')
        self.OptionParser.add_option('--tab_size', action='store',
                                     type='float', dest='tab_size', default=10,
                                     help='Tab size')
        self.OptionParser.add_option('--backlash', action='store',
                                     type='float', dest='backlash', default=0.0,
                                     help='Backlash generated by lasercut')

        self.start_stop = {}

    def effect(self):
        print_(self.options)

        parent = self.current_layer
        centre = self.view_center

        tabs = self.tabs(self.options.width, self.options.tab_size, self.options.thickness, backlash=self.options.backlash * -1, lastUp=True)
        shape = self.getPath(self.toPathString(self.mm2u(tabs)), '%s_bottom' % self.options.path_id, centre[0], centre[1], None, '#FF0000')
        inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), shape)

        tabs = [[0, 0]]
        tabs.extend(self.tabs(self.options.width, self.options.tab_size, self.options.thickness, backlash=self.options.backlash))
        shape = self.getPath(self.toPathString(self.mm2u(tabs)), '%s_bottom' % self.options.path_id, centre[0], centre[1] + 2 * self.mm2u(self.options.thickness), None, '#00FF00')
        inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), shape)


if __name__ == '__main__':
    effect = BoxGeneratorEffect()
    effect.affect()
