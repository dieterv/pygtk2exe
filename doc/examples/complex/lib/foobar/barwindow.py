# -*- coding: utf-8 -*-


import gtk


class BarWindow(gtk.Window):
    __gtype_name__ = 'BarWindow'

    def __init__(self):
        gtk.Window.__init__(self)

        label = gtk.Label('Hello Bar!')
        self.add(label)
