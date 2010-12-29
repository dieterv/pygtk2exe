# -*- coding: utf-8 -*-


import os

from distutils import log
from distutils.dir_util import remove_tree
from distutils.command.clean import clean as _Clean


class Clean(_Clean):
    def initialize_options(self):
        _Clean.initialize_options(self)

        self.dist_dir = None
        self.plat_name = None

    def finalize_options(self):
        _Clean.finalize_options(self)

        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'),
                                            ('plat_name', 'plat_name'))

    def run(self):
        _Clean.run(self)

        if self.all:
            exe_dist_dir = "%s.%s" % (self.distribution.get_fullname(), self.plat_name)
            exe_dist_dir = os.path.join(self.dist_dir, exe_dist_dir)

            if os.path.exists(exe_dist_dir):
                remove_tree(exe_dist_dir, dry_run=self.dry_run)
            else:
                log.warn("'%s' does not exist -- can't clean it", exe_dist_dir)
