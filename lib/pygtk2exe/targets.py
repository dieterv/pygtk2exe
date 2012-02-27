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


from os.path import basename, splitext


class _Target(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        # All generated executables will live in the bin directory to
        # ensure dll files are found where the GTK+ runtime has placed them.
        # Doing this results in a completely self contained package, where
        # you are protected against all known problems with dll files being
        # loaded from unexpected locations (including some directory on PATH,
        # %WINDIR%, %WINDIR%\system, %WINDIR%\system32, PWD, ...)
        if not hasattr(self, 'dest_base'):
            filename = basename(self.script)

            if '.' in filename:
                filename = splitext(filename)[0]

            self.dest_base = 'bin/%s' % filename
        else:
            if '/' in self.dest_base or '\\' in self.dest_base:
                raise
            if not self.dest_base.startswith('bin/'):
                self.dest_base = 'bin/%s' % self.dest_base


class CtypesComServer(_Target):
    pass


class ComServer(_Target):
    pass


class Service(_Target):
    pass


class Windows(_Target):
    pass


class Console(_Target):
    pass


class IsapiFilter(_Target):
    pass
