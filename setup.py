#!/usr/bin/env python

import os
from distutils.command.install_data import install_data
from glob import glob

from setuptools import find_packages, setup

from sr.tools import __description__, __version__


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='sr.tools',
    version=__version__,
    keywords='sr student robotics tools utilities utils',
    url='https://github.com/srobo/tools',
    project_urls={
        'Code': 'https://github.com/srobo/tools',
        'Documentation': 'https://srtools.readthedocs.io/en/latest/',
        'Issue tracker': 'https://github.com/srobo/tools/issues',
    },
    description=__description__,
    long_description=long_description,
    namespace_packages=['sr'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': ['sr = sr.tools.cli:main'],
    },
    author='Student Robotics',
    author_email='info@studentrobotics.org',
    install_requires=[
        'PyYAML >=5, <6',
        'pyparsing >=2.0, <3',
        'BeautifulSoup4 >=4.3, <5',
        'numpy >=1.9, <2',
        'requests >=2.9, <3',
        'six >=1.9, <2',
        'tabulate >=0.7, <1',
        'xlwt-future >=0.8, <1',
    ],
    extras_require={
        'cam-serial, usb-key-serial, sd-serial, mcv4b-part-code': ['pyudev'],
        'price-graph': ['matplotlib'],
        'save passwords': ['keyring'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
)
