#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


# Ensure this example can be used when pygtk2exe is not installed on the system
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib')))

# Ensure py2exe can find the foobar package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))


from distutils.core import setup
from pygtk2exe import Suite, Extension, Console, Windows


suite = Suite(author = 'Monty Python <monty.python@localhost.localnet>',
              company_name = 'Monty Corporation',
              license = 'GPLv3')

_cli = Extension(suite,
                 '_tools',
                 sources=['lib/foobar/_tools.c'])

cli = Console(suite,
              name = 'cli',
              version = '0.0.1',
              description = 'FooBar Administration Tool',
              url = 'http://localhost/FooBar/Cli',
              script = 'bin/cli.py',
              icon_resources = [(1, "share/foobar/system-run.ico")])

bar = Windows(suite,
              name = 'bar',
              version = '1.0.7',
              description = 'Bar Application',
              url = 'http://localhost/FooBar/Bar',
              script = 'bin/bar.py',
              icon_resources = [(1, "share/foobar/system-run.ico")])

foo = Windows(suite,
              name = 'foo',
              version = '1.1.4',
              description = 'Foo Application',
              url = 'http://localhost/FooBar/Foo',
              script = 'bin/foo.py',
              icon_resources = [(1, "share/foobar/system-run.ico")])


#options = {"py2exe": {'dist_dir': 'dist',
#                      'packages': 'foobar'}
options = {'pygtk2exe': {'includes': ['pygtk']}}


if __name__ == '__main__':
    setup(ext_modules = [_cli],
          suite       = suite,
          options     = options)
