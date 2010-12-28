# -*- coding: utf-8 -*-


from __future__ import absolute_import


__all__ = ['Suite', 'Extension', 'CtypesComServer', 'ComServer', 'Service', 'Windows', 'Console', 'IsapiFilter']
__version__ = '0.0.1'


# Silence DeprecationWarnings generated by the py2exe 0.6.9 code
import warnings
warnings.filterwarnings(action='ignore',
                        message='the sets module is deprecated',
                        category=DeprecationWarning,
                        module='py2exe')

# Do a very strict py2exe version check to protect ourselves from the case
# where we should become incompatible with what future py2exe versions may expect.
from py2exe import __version__ as py2exe_version

if not py2exe_version == '0.6.9':
    raise ImportError('pygtk2exe requires py2exe 0.6.9 but found %s' % py2exe_version)

# Replace the py2exe command.
from pygtk2exe.command import build_exe
# Replace distutils' Distribution class
from pygtk2exe import dist

# Keep our "namespace" clean
del warnings
del py2exe_version
del build_exe
del dist

# Make everything usable in setup.py scripts available
from pygtk2exe.targets import Suite, Extension, CtypesComServer, ComServer, Service, Windows, Console, IsapiFilter
