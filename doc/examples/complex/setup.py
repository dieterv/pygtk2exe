#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


# Ensure this example can be used when pygtk2exe is not installed on the system
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib')))

# Ensure py2exe can find the foobar package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))


from distutils.core import setup
from distutils.extension import Extension
from pygtk2exe import Console, Windows


_cli = Extension('_tools',
                 sources=['lib/foobar/_tools.c'])

cli = Console(name = 'cli',
              version = '0.0.1',
              description = 'FooBar Administration Tool',
              url = 'http://localhost/FooBar/Cli',
              script = 'bin/cli.py',
              icon_resources = [(1, "share/foobar/system-run.ico")])

bar = Windows(name = 'bar',
              version = '1.0.7',
              description = 'Bar Application',
              url = 'http://localhost/FooBar/Bar',
              script = 'bin/bar.py',
              icon_resources = [(1, "share/foobar/system-run.ico")])

foo = Windows(name = 'foo',
              version = '1.1.4',
              description = 'Foo Application',
              url = 'http://localhost/FooBar/Foo',
              script = 'bin/foo.py',
              icon_resources = [(1, "share/foobar/system-run.ico")])


options = {'pygtk2exe': {'includes': ['pygtk']}}


setup(name         = 'complex example',
      version      = '0.0.1',
      description  = 'complex pygtk2exe example',
      author       = 'Monty Python',
      classifiers  = ['Development Status :: 1 - Planning',
                      'Environment :: X11 Applications :: GTK',
                      'Intended Audience :: Developers',
                      'Programming Language :: Python',
                      'Topic :: Software Development :: Libraries :: Python Modules'],
      ext_modules = [_cli],
      console     = [cli],
      windows     = [bar, foo],
      options     = options
      )
