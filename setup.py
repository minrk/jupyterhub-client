#-----------------------------------------------------------------------------
#  Copyright (C) Min RK
#
#  Distributed under the terms of the 2-clause BSD License.
#-----------------------------------------------------------------------------

from __future__ import print_function


import os
import sys

from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.test import test as TestCommand

name = 'jupyterhub-client'
pkg_name = name.replace('-', '_')

class EggsNotAllowed(bdist_egg):
    """
    Never build eggs.
    """
    description = "Building eggs is disabled"
    def run(self):
        sys.exit("Refusing to build eggs. Use `pip install`")


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--cov', pkg_name]
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)


with open(os.path.join(pkg_name, '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__'):
            __version__ = eval(line.split('=', 1)[1])
            break


setup_args = dict(
    name = name,
    version = __version__,
    packages = [pkg_name],
    author = "Min Ragan-Kelley",
    author_email = "benjaminrk@gmail.com",
    url = 'http://github.com/minrk/jupyterhub-client',
    description = "Client for JupyterHub REST API",
    long_description = "",
    license = "BSD",
    install_requires = [
        'requests',
        'tornado>=4.1',
    ],
    cmdclass = {
        'bdist_egg': EggsNotAllowed,
        'test': PyTest,
    },
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)

setup(**setup_args)

