#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='sr.tools',
    version='1.0.0',
    keywords='sr student robotics tools utilities utils',
    url='https://www.studentrobotics.org/trac/wiki/DevScripts',
    description='Student Robotics Tools',
    long_description=long_description,
    namespace_packages=['sr'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': ['sr = sr.tools.cli:main']
    },
    install_requires=[
        'PyYAML >=3.11, <4',
        'sympy >=0.7, <1',
        'pyparsing >=2.0, <3',
        'BeautifulSoup4 >=4.3, <5',
        'numpy >=1.9, <2',
        'six >=1.9, <2',
        'tabulate >=0.7, <1',
        'xlwt-future >=0.8, <1'
    ],
    setup_requires=[
        'Sphinx >=1.3, <2',
        'Pygments >=2.0, <3',
        'nose >=1.3, <2',
        'numpy >=1.9, <2'  # https://github.com/numpy/numpy/issues/2434#issuecomment-65252402
    ],
    extras_require={
        'cam-serial, usb-key-serial, sd-serial, mcv4b-part-code': ['pyudev'],
        'price-graph': ['matplotlib'],
        'save passwords': ['keyring']
    },
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ],
    test_suite='nose.collector'
)
