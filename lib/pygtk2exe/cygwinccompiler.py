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


from distutils.cygwinccompiler import Mingw32CCompiler as _Mingw32CCompiler


# 1) We want to built code compatible with the GTK+ runtime, where
#    MSVC compatible struct packing is required.
# 2) http://bugs.python.org/issue12641 might eventually get fixed
#    in Python 2.7, 3.2 and 3.3 but there is no hope for 2.6, so
#    let's fix it ourselves, remove -mno-cygwin and be done with it.

class Mingw32CCompiler(_Mingw32CCompiler):
    def __init__(self, verbose=0, dry_run=0, force=0):
        _Mingw32CCompiler.__init__(self, verbose=0, dry_run=0, force=0)

        # ld_version >= "2.13" support -shared so use it instead of
        # -mdll -static
        if self.ld_version >= "2.13":
            shared_option = "-shared"
        else:
            shared_option = "-mdll -static"

        # A real mingw32 doesn't need to specify a different entry point,
        # but cygwin 2.91.57 in no-cygwin-mode needs it.
        if self.gcc_version <= "2.91.57":
            entry_point = '--entry _DllMain@12'
        else:
            entry_point = ''

        self.set_executables(compiler='gcc -O -mms-bitfields -Wall',
                             compiler_so='gcc -mms-bitfields -mdll -O -Wall',
                             compiler_cxx='g++ -mms-bitfields -O -Wall',
                             linker_exe='gcc',
                             linker_so='%s %s %s' % (self.linker_dll, shared_option, entry_point))

