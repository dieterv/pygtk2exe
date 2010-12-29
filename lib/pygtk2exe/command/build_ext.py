# -*- coding: utf-8 -*-


import os

from dsextras import BuildExt as _build_ext


class build_ext(_build_ext):
    def run(self):
        _build_ext.run(self)

        # This makes sure py2exe can locate the extension we've built
        build_lib = os.path.abspath(self.build_lib)
        os.environ['PATH'] = '%s%s%s' % (build_lib, os.pathsep, os.environ['PATH'])
