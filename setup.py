#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='sportsstats',
    version='0.1.0',
    description="Tools for downloading sports statistics.",
    long_description=readme + '\n\n' + history,
    author="William Myers",
    author_email='mwilliammyers+pypi@gmail.com',
    url='https://github.com/mwilliammyers/sportsstats',
    packages=[
        'sportsstats',
    ],
    package_dir={
        'sportsstats': 'sportsstats'
    },
    scripts=[
        'bin/stats',
    ],
    include_package_data=True,
    install_requires=[],
    license="GPL-3.0",
    zip_safe=False,
    keywords='sportsstats stats statistics sports',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License version 3.0 (GPL-3.0)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=[]
)
