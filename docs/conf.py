import glob
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from sr.tools import __version__


needs_sphinx = '1.3'  # for Napoleon

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'Student Robotics Tools'
copyright = '2014, Student Robotics'

version = __version__
release = __version__

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'StudentRoboticsToolsdoc'


latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'preamble': '\\setcounter{tocdepth}{2}'
}

latex_documents = [
    (
        'index',  # source start file
        'StudentRoboticsTools.tex',  # target name
        'Student Robotics Tools Documentation',  # title
        'Student Robotics',  # author
        'manual',  # document class
    ),
]


man_pages = []
for f in glob.glob('commands/*.rst'):
    if 'index.rst' in f:
        continue  # we don't want this in the man pages
    command_name = f[9:-4]
    name = 'sr-{}'.format(command_name)
    description = 'Help for "{}" tool.'.format(command_name)
    man_pages.append((f[:-4], name, description, ['Student Robotics'], 1))


texinfo_documents = [
  ('index', 'StudentRoboticsTools', 'Student Robotics Tools Documentation',
   'Student Robotics', 'StudentRoboticsTools', 'One line description of project.',
   'Miscellaneous'),
]


intersphinx_mapping = {'http://docs.python.org/': None}
