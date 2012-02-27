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

from dsextras import BuildExt as _build_ext


class build_ext(_build_ext):
    def run(self):
        _build_ext.run(self)

        # This makes sure py2exe can locate the extension we've built
        build_lib = os.path.abspath(self.build_lib)
        os.environ['PATH'] = '%s%s%s' % (build_lib, os.pathsep, os.environ['PATH'])
