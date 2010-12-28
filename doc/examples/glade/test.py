#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

import gtk
import gtk.glade


if __name__ == '__main__':
    if hasattr(sys, 'frozen'):
        path = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
    else:
        path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))

    gladefile = os.path.join(path, 'test.glade')

    wtree = gtk.glade.XML(gladefile)
    window = wtree.get_widget("window1")
    window.connect('delete-event', gtk.main_quit)
    window.show_all()

    gtk.main()
