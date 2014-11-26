#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name='sr.tools',
    version='1.0.0-dev',
    keywords='sr student robotics',
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
        'six'
    ],
    extras_require={
        'inv-history': ['pygit2'],
        'linux': ['pyudev'],
        'price-graph': ['matplotlib']
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ],
    test_suite='tests'
)
