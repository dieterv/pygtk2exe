#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gtk


if __name__ == '__main__':
    window = gtk.Window()
    window.connect('delete-event', gtk.main_quit)
    window.set_title('Shiny application')
    label = gtk.Label('Hello!')
    window.add(label)
    window.show_all()

    gtk.main()
