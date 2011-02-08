# -*- coding: utf-8 -*-


from distutils.dist import Distribution as _Distribution

from pygtk2exe.command.clean import clean
from pygtk2exe.command.build_ext import build_ext
from pygtk2exe.command.build_exe import py2exe


class ConfigurationError(Exception):
    pass


class Distribution(_Distribution):
    def __init__(self, attrs):
        # Set keywords and options
        self.validate_keywords(attrs)
        self.set_keywords(attrs)
        self.validate_options(attrs)
        self.set_options(attrs)

        # Initialize base class
        _Distribution.__init__(self, attrs)

        # Replace distutils commands
        self.cmdclass['clean'] = clean
        self.cmdclass['build_ext'] = build_ext
        self.cmdclass['py2exe'] = py2exe

    def validate_keywords(self, attrs):
        # pygtk2exe takes control of all py2exe specific keywords passed to
        # the setup function, so we raise an error if the user mistakenly passes
        # one of those keywords along with his setup() function call.
        if attrs.has_key('zipfile'):
            raise ConfigurationError('The "zipfile" keyword should not be passed '
                                     'directly to your setup() function. This will '
                                     'be automatically configured by pygtk2exe.')

    def set_keywords(self, attrs):
        if not attrs.has_key('data_files'):
            attrs['data_files'] = []

        # py2exe specific keywords
        self.zipfile = 'bin/library.zip'

        if not hasattr(self, 'ext_modules'):
            self.ext_modules = []

        if not hasattr(self, 'ctypes_com_server'):
            self.ctypes_com_server = []

        if not hasattr(self, 'com_server'):
            self.com_server = []

        if not hasattr(self, 'service'):
            self.service = []

        if not hasattr(self, 'windows'):
            self.windows = []

        if not hasattr(self, 'console'):
            self.console = []

        if not hasattr(self, 'isapi'):
            self.isapi = []


    def validate_options(self, attrs):
        '''
        pygtk2exe takes control of all py2exe specific options passed to the
        setup function via the options keyword, so we raise an error if the
        user mistakenly passes py2exe options along with his setup() function
        call.
        '''
        if attrs.has_key('options'):
            if not attrs['options'].has_key('pygtk2exe'):
                raise ConfigurationError('The "options" keyword should at least contain the '
                                         'pygtk2exe "includes" option, specifying either '
                                         '"pygobject" or "pygtk".')

        includes = attrs['options']['pygtk2exe']['includes']

        if 'pygobject' in includes and 'pygtk' in includes:
            raise ConfigurationError('The "includes" option should not contain '
                                     'both "pygobject" and "pygtk" at the same time.')

        if not 'pygobject' in includes and not 'pygtk' in includes:
            raise ConfigurationError('The "includes" option should contain either '
                                     '"pygobject" or "pygtk".')

    def set_options(self, attrs):
        # includes
        includes = attrs['options']['pygtk2exe']['includes']

        if 'pygobject' in includes:
            includes.remove('pygobject')
            includes.extend(['glib', 'gio', 'gobject'])
        elif 'pygtk' in includes:
            includes.remove('pygtk')
            includes.extend(['glib', 'gio', 'gobject', 'cairo', 'atk', 'pango', 'pangocairo', 'gtk'])

        # py2exe has some trouble with gdk
        if 'gtk' in includes:
            ignores = []
            ignores.append('gdk')

        # py2exe has some trouble with glib (that's what we get with wild imports...)
        if 'glib' in includes:
            import glib

            for name in dir(glib):
                if not (name.startswith('__') and name.endswith('__')):
                    ignores.append('glib.%s' % name)

        # Construct and return options dict
        attrs['options']['py2exe'] = {'dll_excludes': 'w9xpopen.exe',
                                      'ignores': ignores,
                                      'includes': includes}
