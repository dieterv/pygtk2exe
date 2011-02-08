# -*- coding: utf-8 -*-


import os

from copy import copy

from distutils.extension import Extension

from py2exe.build_exe import py2exe as _py2exe
from py2exe.py2exe_util import depends
from pygtk2exe.targets import CtypesComServer, ComServer, Service, Windows, Console, IsapiFilter


class ConfigurationError(Exception):
    pass


class py2exe(_py2exe):
    description = 'create a self-contained executable package for MS Windows'

    def __init__(self, dist):
        _py2exe.__init__(self, dist)

    def initialize_options(self):
        _py2exe.initialize_options(self)

        self.plat_name = None

    def finalize_options(self):
        _py2exe.finalize_options(self)

        self.set_undefined_options('bdist', ('plat_name', 'plat_name'))

    def _initialize_distribution(self):
        # prevent py2exe from clobbering the dist dir
        exe_dist_dir = "%s.%s" % (self.distribution.get_fullname(), self.plat_name)
        self.dist_dir = os.path.join(self.dist_dir, exe_dist_dir)

        # Merge data_files for each Target into the data_files keyword
        targets = self.distribution.ctypes_com_server + \
                  self.distribution.com_server + \
                  self.distribution.service + \
                  self.distribution.windows + \
                  self.distribution.console + \
                  self.distribution.isapi

        for target in targets:
            if hasattr(target, 'data_files'):
                targetdirs = [x[0] for x in self.distribution.data_files]

                for (targetdir, files) in target.data_files:
                    if not targetdir in targetdirs:
                        self.distribution.data_files.append((targetdir, files))
                    else:
                        for file in files:
                            index = targetdirs.index(targetdir)

                            if not file in self.distribution.data_files[index]:
                                self.distribution.data_files[index][1].append(file)

    def run(self):
        self._initialize_distribution()
        _py2exe.run(self)

    def copy_dlls(self, dlls):
        '''
        Extend the copy_dlls method so we can teach it how to handle GTK+ and friends.
        This is where the magic happens :)
        '''

        print '*** collecting GTK+ runtime dependencies ***'

        # Where does the GTK+ runtime live?
        PATH = os.environ['PATH'].split(os.pathsep)

        for path in PATH:
            gtk_root = os.path.abspath(os.path.join(path, '..'))
            gtk_bindir = os.path.join(gtk_root, 'bin')
            gtk_manifestdir = os.path.join(gtk_root, 'manifest')

            # TODO: This test could use some improvements, but how?
            if os.path.isdir(gtk_bindir) and os.path.isdir(gtk_manifestdir):
                break
        else:
            raise SystemExit('Error: No suitable GTK+ runtime has been found.')

        # Collect GTK+ runtime manifest data
        manifestdata = {}

        for root, dirs, files in os.walk(gtk_manifestdir):
            for manifestfile in files:
                # Get .exe and .dll files from this package
                manifest_dlls = []
                manifestfile = os.path.abspath(os.path.join(root, manifestfile))

                f = open(manifestfile, 'rU')

                for line in f:
                    line = line.strip()
                    dirname = os.path.dirname(line)
                    filename = os.path.basename(line)
                    manifest_dlls.append((dirname, filename))

                f.close()

                manifestdata[manifestfile] = manifest_dlls

        # Get dlls that belong to the GTK+ runtime
        gtk_dlls = []

        for dll in copy(dlls):
            dllfile = os.path.abspath(dll)
            dllfilename = os.path.basename(dllfile)

            if os.path.isfile(os.path.join(gtk_bindir, dllfilename)):
                # py2exe no longer needs to worry about this file
                dlls.remove(dll)

                # because we take care of it
                gtk_dlls.append(dllfilename)

        # Match GTK+ dlls to manifests
        gtk_manifests = []

        for manifest, value in manifestdata.iteritems():
            for dirname, filename in value:
                if filename in gtk_dlls:
                    if not manifest in gtk_manifests:
                        gtk_manifests.append(manifest)

        # Get extra dependencies for .dll and .exe files included in the manifest
        # files we collected above
        extra_dlls = []

        for manifest, value in manifestdata.iteritems():
            if manifest in gtk_manifests:
                for dirname, filename in value:
                    if filename.endswith('.exe') or filename.endswith('.dll'):

                        #for dll, uses_import_module in depends(image, loadpath).items()
                        for dll, uses_import_module in depends(filename, os.path.join(gtk_root, dirname)).items():
                            dllfilename = os.path.basename(dll)

                            if not dllfilename in gtk_dlls and not dllfilename in extra_dlls:
                                extra_dlls.append(dllfilename)

        # Match extra dlls to manifests
        extra_manifests = []

        for manifest, value in manifestdata.iteritems():
            for dirname, filename in value:
                if filename in copy(extra_dlls):
                    if not manifest in extra_manifests and not manifest in gtk_manifests:
                        # py2exe no longer needs to worry about this file
                        extra_dlls.remove(filename)

                        # because we take care of it
                        extra_manifests.append(manifest)

        gtk_manifests.extend(extra_manifests)

        # Let py2exe copy dll files not handles by pygtk2exe
        _py2exe.copy_dlls(self, dlls)

        # Finally, copy GTK+ dependencies
        print '*** copy GTK+ runtime dependencies ***'

        for manifest in gtk_manifests:
            for dirname, filename in manifestdata[manifest]:
                src = os.path.join(gtk_root, dirname, filename)
                dst = os.path.join(self.dist_dir, dirname, filename)
                dstdir = os.path.join(self.dist_dir, dirname)

                if not os.path.isdir(dstdir):
                    os.makedirs(dstdir)

                self.copy_file(src, dst, preserve_mode=False, preserve_times=True)

            # TODO: Not sure if the following is ideal. But we cannot rely on the
            # manifest files to be complete for configuration files...
            done = []

            for dirname, filename in manifestdata[manifest]:
                if dirname.startswith('etc'):
                    if not dirname in done:
                        done.append(dirname)

                        # TODO: Does not do a recursive copy...
                        for filename in os.listdir(os.path.join(gtk_root, dirname)):
                            src = os.path.join(gtk_root, dirname, filename)

                            if os.path.isfile(src):
                                dst = os.path.join(self.dist_dir, dirname, filename)
                                dstdir = os.path.join(self.dist_dir, dirname)

                                if not os.path.isdir(dstdir):
                                    os.makedirs(dstdir)

                                self.copy_file(src, dst, preserve_mode=False, preserve_times=True)
