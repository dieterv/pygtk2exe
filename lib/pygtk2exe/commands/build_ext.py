# -*- coding: utf-8 -*-


import os

from dsextras import BuildExt as _BuildExt


class BuildExt(_BuildExt):
    def run(self):
        _BuildExt.run(self)

        # This makes sure py2exe can locate the extension we've built
        build_lib = os.path.abspath(self.build_lib)
        os.environ['PATH'] = '%s%s%s' % (build_lib, os.pathsep, os.environ['PATH'])
