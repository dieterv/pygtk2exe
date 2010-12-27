# -*- coding: utf-8 -*-


import gtk


class FooWindow(gtk.Window):
    __gtype_name__ = 'FooWindow'

    def __init__(self):
        gtk.Window.__init__(self)

        label = gtk.Label('Hello Foo!')
        self.add(label)
