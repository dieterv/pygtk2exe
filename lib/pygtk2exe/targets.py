# -*- coding: utf-8 -*-


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
