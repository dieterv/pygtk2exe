# -*- coding: utf-8 -*-


from distutils.dist import Distribution as _Distribution

from pygtk2exe.commands.build_ext import BuildExt
from pygtk2exe.targets import Extension, CtypesComServer, ComServer, Service, Windows, Console, IsapiFilter


class ConfigurationError(Exception):
    pass


class Distribution(_Distribution):
    def __init__(self, attrs):
        # pygtk2exe takes control of all py2exe specific keywords passed to
        # the setup function, so we raise an error if the user mistakenly passes
        # one of those keywords along with his setup() function call.
        if attrs.has_key('zipfile'):
            raise ConfigurationError('The "zipfile" keyword should not be passed '
                                     'directly to your setup() function. This will '
                                     'be automatically configured by pygtk2exe.')

        keywords = ['ctypes_com_server', 'com_server', 'service', 'windows', 'console', 'isapi']

        for keyword in keywords:
            if attrs.has_key(keyword):
                raise ConfigurationError('The "%s" keyword should not be passed '
                                         'directly to your setup() function. Please '
                                         'use the pygtk2exe provided alternative.' % keyword)

        # set py2exe specific keywords
        self.zipfile = 'bin/library.zip'
        self.ext_modules = []
        self.ctypes_com_server = []
        self.com_server = []
        self.service = []
        self.windows = []
        self.console = []
        self.isapi = []

        if attrs.has_key('suite'):
            suite = attrs.pop('suite')

            for target in suite.targets:
                if isinstance(target, Extension):
                    self.ext_modules.append(target),
                elif isinstance(target, CtypesComServer):
                    self.ctypes_com_server.append(target)
                elif isinstance(target, ComServer):
                    self.com_server.append(target)
                elif isinstance(target, Service):
                    self.service.append(target)
                elif isinstance(target, Windows):
                    self.windows.append(target)
                elif isinstance(target, Console):
                    self.console.append(target)
                elif isinstance(target, IsapiFilter):
                    self.isapi.append(target)
        else:
            raise AttributeError('pygtk2exe expects you to configure a suite')

        # pygtk2exe takes control of all py2exe specific options passed to the
        # setup function via the options keyword, so we raise an error if the
        # user mistakenly passes py2exe options along with his setup() function
        # call.
        if attrs.has_key('options'):
            if attrs['options'].has_key('py2exe'):
                raise ConfigurationError('The "options" keyword should not contain '
                                         'py2exe options. This will be automatically '
                                         'configured by pygtk2exe.')
        else:
            attrs['options'] = {}

        # py2exe has some trouble with gdk
        ignores = []
        ignores.append('gdk')

        # py2exe has some trouble with glib (that's what we get with wild imports...)
        import glib

        for name in dir(glib):
            if not (name.startswith('__') and name.endswith('__')):
                ignores.append('glib.%s' % name)

        attrs['options']['py2exe'] = {'dll_excludes': 'w9xpopen.exe',
                                      'ignores': ignores}

        # Initialize base class
        _Distribution.__init__(self, attrs)

        # Replace the build_ext command
        self.cmdclass['build_ext'] = BuildExt

        # Run "clean" and "py2exe" commands by default
        if not self.script_args:
            self.script_args.append('clean')
            self.script_args.append('py2exe')


# Replace distutils.core.Distribution with our own Distribution class
import distutils
distutils.core.Distribution = Distribution
