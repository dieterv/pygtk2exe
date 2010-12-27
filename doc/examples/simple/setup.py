#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


# Ensure this example can be used when pygtk2exe is not installed on the system
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib')))


from distutils.core import setup
from pygtk2exe import Suite, Windows


suite = Suite(author = 'Monty Python <monty.python@localhost.localnet>',
              company_name = 'Monty Corporation',
              license = 'GPLv3')

test = Windows(suite,
               name = 'test',
               version = '0.0.1',
               description = 'Test Application',
               url = 'http://localhost/Test/',
               script = 'test.py',
               data_files = [('bin', ['test.exe.manifest'])]
               )


if __name__ == '__main__':
    setup(suite = suite)
