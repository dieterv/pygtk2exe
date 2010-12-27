#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gobject
import foobar


def quit(widget, event, mainloop):
    mainloop.quit()


if __name__ == '__main__':
    # Initialize mainloop
    gobject.threads_init()
    mainloop = gobject.MainLoop()

    # Initialize FooWindow
    mainwindow = foobar.FooWindow()
    mainwindow.connect('delete-event', quit, mainloop)
    mainwindow.show_all()

    # Run mainloop
    mainloop.run()
