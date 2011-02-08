#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


# Ensure this example can be used when pygtk2exe is not installed on the system
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib')))


from distutils.core import setup
from pygtk2exe import Windows


test = Windows(name = 'test',
               version = '0.0.1',
               description = 'Test Application',
               url = 'http://localhost/Test/',
               author = 'Monty Python <monty.python@localhost.localnet>',
               company_name = 'Monty Corporation',
               license = 'GPLv3',
               script = 'test.py')


options = {'pygtk2exe': {'includes': ['pygtk']}}


setup(name         = 'simple-example',
      version      = '0.0.1',
      description  = 'simple pygtk2exe example',
      author       = 'Monty Python',
      license      = 'GPLv3',
      classifiers  = ['Development Status :: 1 - Planning',
                      'Environment :: X11 Applications :: GTK',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                      'Programming Language :: Python',
                      'Topic :: Software Development :: Libraries :: Python Modules'],
      windows      = [test],
      options      = options)
