#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import sys

from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

#  needs_detox = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
#  pytest_runner = ['pytest-runner'] if needs_pytest else []

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='sportsstats',
    version='0.1.3',
    description="Tools for downloading sports statistics.",
    long_description=readme,
    author="William Myers",
    author_email='mwilliammyers+pypi@gmail.com',
    url='https://github.com/mwilliammyers/sportsstats',
    packages=find_packages('lib'),
    package_dir={
        '': 'lib',
    },
    scripts=[
        'bin/stats',
    ],
    include_package_data=True,
    install_requires=[
        'nba_py'
    ],
    license="GPLv3+",
    zip_safe=False,
    keywords='sportsstats stats statistics sports',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    #  setup_requires=[
    #  ] + pytest_runner,
    test_suite='tests',
        #  'pytest',
        #  'pytest-flake8',
        #  'pytest-cov',
    tests_require=[
        'tox'
    ],
    cmdclass = {
        'test': Tox
    },
    dependency_links=[
        'http://github.com/mwilliammyers/nba_py/tarball/master#egg=nba_py'
    ]
)
