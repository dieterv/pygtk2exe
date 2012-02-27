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

from distutils import log
from distutils.dir_util import remove_tree
from distutils.command.clean import clean as _clean


class clean(_clean):
    def initialize_options(self):
        _clean.initialize_options(self)

        self.dist_dir = None
        self.plat_name = None

    def finalize_options(self):
        _clean.finalize_options(self)

        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'),
                                            ('plat_name', 'plat_name'))

    def run(self):
        _clean.run(self)

        if self.all:
            exe_dist_dir = "%s.%s" % (self.distribution.get_fullname(), self.plat_name)
            exe_dist_dir = os.path.join(self.dist_dir, exe_dist_dir)

            if os.path.exists(exe_dist_dir):
                remove_tree(exe_dist_dir, dry_run=self.dry_run)
            else:
                log.warn("'%s' does not exist -- can't clean it", exe_dist_dir)
