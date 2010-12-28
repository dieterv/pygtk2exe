# -*- coding: utf-8 -*-


import os

from distutils.dir_util import remove_tree
from distutils.command.clean import clean as _Clean


class Clean(_Clean):
    description = 'clean up temporary files from "build" command'

    user_options = _Clean.user_options
    user_options.append(('aggressive', None, 'removes all build output from the build and dist directories'))

    boolean_options = _Clean.boolean_options
    boolean_options.append('aggressive')

    def initialize_options(self):
        _Clean.initialize_options(self)

        self.dist_dir = None
        self.aggressive = None

    def finalize_options(self):
        _Clean.finalize_options(self)

        self.set_undefined_options('bdist',
                                   ('dist_dir', 'dist_dir'))
    def run(self):
        if not self.aggressive:
            _Clean.run(self)
        else:
            clean = [os.path.abspath(self.build_base), os.path.abspath(self.dist_dir)]

            for directory in clean:
                if os.path.exists(directory):
                    remove_tree(directory, dry_run=self.dry_run)
