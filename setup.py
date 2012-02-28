#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2010-2012 pygtk2exe Contributors
#
# This file is part of pygtk2exe.
#
# pygtk2exe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pygtk2exe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pygtk2exe. If not, see <http://www.gnu.org/licenses/>.


import os
import re
import fnmatch

from ez_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def version():
    file = os.path.join(os.path.dirname(__file__), 'lib', 'pygtk2exe', '__init__.py')
    return re.compile(r".*__version__ = '(.*?)'", re.S).match(read(file)).group(1)

def _get_data_files(dest, src, filter):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), src))
    files = []

    if os.path.isdir(path):
        for item in fnmatch.filter(os.listdir(path), filter):
            if os.path.isfile(os.path.join(path, item)):
                files.append(('%s/%s' % (src, item)))
    else:
        print 'get_data_files: "%s" does not exist, ignoring' % src

    return files

def get_data_files(*args):
    data_files = []

    for (dest, src, filter) in args:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), src))

        if os.path.isdir(path):
            data_files.append(('%s' % dest, _get_data_files('%s' % dest, '%s' % src, filter)))

            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)):
                    data_files.append(('%s/%s' % (dest, item), _get_data_files('%s/%s' % (dest, item), '%s/%s' % (src, item), filter)))
        else:
            print 'get_data_files: "%s" does not exist, ignoring' % src

    return data_files


setup(name = 'pygtk2exe',
      version = version(),
      description = 'Extra py2exe distutils extensions to convert PyGObject/PyGTK Python scripts into executable Windows programs.',
      long_description = read('README'),
      author = 'pygtk2exe Contributors',
      #author_email = 'pygtk2exe-list@googlegroups.com', #TODO: create list
      url = 'http://github.com/dieterv/pygtk2exe/',
      download_url = 'http://github.com/dieterv/pygtk2exe/downloads/',
      license = 'GNU General Public License',
      classifiers = ['Development Status :: 5 - Production/Stable',
                    'Environment :: X11 Applications :: GTK',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Natural Language :: English',
                    'Operating System :: Microsoft :: Windows',
                    'Programming Language :: Python',
                    'Topic :: Software Development :: Build Tools',
                    'Topic :: Software Development :: Libraries :: Python Modules'],

      install_requires = ['setuptools',
                          'py2exe == 0.6.9'],
      zip_safe = False,
      include_package_data = True,

      packages = find_packages('lib'),
      package_dir = {'': 'lib'},
      data_files = get_data_files(('doc/examples', 'doc/examples', '*'))
      )
