#!/usr/bin/env python

import os
from distutils.command.install_data import install_data
from glob import glob

from setuptools import setup


class install_data_with_sphinx(install_data):
    def run(self):
        self.run_command('build_sphinx')
        self.data_files.remove('docs')
        sphinx = self.get_finalized_command('build_sphinx')
        self.data_files += [
            ('share/man/man1', glob(os.path.join(sphinx.build_dir, 'man', '*.1'))),
        ]
        install_data.run(self)


setup(
    cmdclass={
        'install_data': install_data_with_sphinx,
    },
    data_files=[
        'docs',  # there has to be an entry for 'install_data' to run
    ],
)
