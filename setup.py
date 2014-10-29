#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name="sr-tools",
    version="1.0.0-dev",
    keywords="sr student robotics",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["sr = sr.cli:main"]
    },
    install_requires=[
        "PyYaml"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities"
    ]
)
