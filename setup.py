#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of PyHunspell.

PyHunspell is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyHunspell is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyHunspell.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.core import setup, Extension
import os
import platform
from glob import glob
import re

def form_possible_names(lib, exts):
    ret = []
    for ext in exts:
        ret.append("%s*%s" % (lib, ext))
    for ext in exts:
        ret.append("lib%s*%s" % (lib, ext))
    return ret

def get_library_name(lib):
    paths = [
      '/usr/local/lib64',
      '/usr/local/lib',
      '/usr/local/libdata',
      '/opt/local/lib',
      '/usr/lib64',
      '/usr/lib',
      '/usr/X11/lib',
      '/usr/share',
    ]
    acceptable_exts = [
        "",
        ".so"
    ]

    if platform.system() == "Windows":
        acceptable_exts = [
            "",
            ".dll",
            ".dll.a"
        ]
        paths = list(set([
            os.path.dirname(__file__),
            os.path.abspath(os.curdir),
            os.path.join(os.environ.get("SystemRoot"), "system"),
            os.path.join(os.environ.get("SystemRoot"), "system32"),
            os.environ.get("SystemRoot"),
        ]))
        try:
            while True:
                paths.remove(None)
        except ValueError:
            pass
        paths.extend(list(set(os.environ.get('PATH').split(os.path.pathsep))))
    elif platform.system() == "Darwin":
        acceptable_exts.append(".dylib")

    names = form_possible_names(lib, acceptable_exts)

    for pn in paths:
        globbed = []
        for name in names:
            if name.find("*") >= 0:
                globbed.extend(glob(os.path.join(pn, name)))
            else:
                globbed.append(os.path.join(pn, name))
        for filepath in globbed:
            if os.path.isfile(filepath) and (os.path.splitext(filepath)[-1] in acceptable_exts):
                return filepath
    return None

libraries=["hunspell"]

hunspell_lib = get_library_name("hunspell")
if hunspell_lib:
    libraries=[re.sub(r"^lib|.dylib$|.so$|.dll$|.dll.a$|.a$", "", hunspell_lib.split(os.path.sep)[-1])]

include_dirs = [
    '/usr/local/include/hunspell',
    '/opt/include/hunspell',
    '/usr/include/hunspell'
]

main = Extension('hunspell',
                 define_macros=[('_LINUX', None)],
                 libraries=libraries,
                 include_dirs=include_dirs,
                 sources=['hunspell.c'],
                 extra_compile_args=['-Wall'])

setup(name="hunspell",
      version="0.2.1",
      description="Module for the Hunspell spellchecker engine",
      author="Benoît Latinier",
      author_email="benoit@latinier.fr",
      url="http://github.com/blatinier/pyhunspell",
      ext_modules=[main])
