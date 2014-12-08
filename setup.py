#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name='sr.tools',
    version='1.0.0-dev',
    keywords='sr student robotics tools utilities utils',
    namespace_packages=['sr'],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['sr = sr.tools.cli:main']
    },
    install_requires=[
        'pyyaml',
        'sympy',
        'pyparsing',
        'beautifulsoup4',
        'numpy',
        'six',
        'xlwt-future'
    ],
    extras_require={
        'cam-serial, usb-key-serial, sd-serial, mcv4b-part-code': ['pyudev'],
        'price-graph': ['matplotlib']
    },
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ]
)
