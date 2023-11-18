#!/usr/bin/env python

import os
from distutils.command.install_data import install_data
from glob import glob

from setuptools import find_packages, setup

from sr.tools import __description__, __version__


class install_data_with_sphinx(install_data):
    def run(self):
        self.run_command('build_sphinx')
        self.data_files.remove('docs')
        sphinx = self.get_finalized_command('build_sphinx')
        self.data_files += [
            ('share/man/man1', glob(os.path.join(sphinx.build_dir, 'man', '*.1'))),
        ]
        install_data.run(self)


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
        'PyYAML >=5, <7',
        'pyparsing >=2.0, <3',
        'BeautifulSoup4 >=4.3, <5',
        'numpy >=1.9, <2',
        'requests >=2.9, <3',
        'six >=1.9, <2',
        'tabulate >=0.7, <1',
        'xlwt-future >=0.8, <1',
    ],
    setup_requires=[
        # Note: Sphinx needs to be manually installed before running `setup.py`
        # to avoid issues importing `sphinxcontrib.applehelp`.
        'Sphinx >=2, <7',
        'Pygments >=2.0, <3',
    ],
    extras_require={
        'cam-serial, mcv4b-part-code': ['pyudev'],
        'price-graph': ['matplotlib'],
        'save-passwords': ['keyring'],
    },
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'install_data': install_data_with_sphinx,
    },
    data_files=[
        'docs',  # there has to be an entry for 'install_data' to run
    ],
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
    ],
)
