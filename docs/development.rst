Development
===========

Here are some instructions to aid development of the tools.

Adding new tools
----------------

Adding a new tool is a fairly straightforward process. First you need to pick
which group the tool lives under. The groups can be found in the
``sr/tools/cli`` directory in the source code. If you need to create a new
group, see the instructions in the next section.

Next you will create a Python file in the directory of the group you have
chosen which should be the same name as the tool when invoked except that
dashes should be replaced with underscores. In that file you should create a
function, typically named ``command``, which accepts a single argument which
will contain the argument ``Namespace`` object from ``argparse``. You will also
need a second function, called ``add_subparser`` which accepts an ``argparse``
subparser object and can be used to set up the argument parsing for that
particular command. It is important that somewhere in that function you set the
default value of ``func`` to the command function you create first. An empty
command file would look something like this:

.. code::

    def command(args):
        if not args.quiet:
            print(args)


    def add_subparser(subparsers):
        parser = subparsers.add_parser('print-args')
        parser.add_argument('--quiet', '-q', action='store_true', dest='quiet')
        parser.set_defaults(func=command)

Finally, you should make sure to include the new file in the ``__all__`` list
of the ``__init__.py`` file from the group you chose.

Adding a new tool group
~~~~~~~~~~~~~~~~~~~~~~~

If you find yourself needing to create a new group to hold a command, you
should first create a directory for it with an empty ``__init.py__`` file.

Next move to the ``__init__.py`` file for the ``sr.tools.cli`` module and add
the new group to the import statement near the top. Finally, in the ``main``
function, you should add a line that looks something like this:

.. code::

    add_subcommands(my_awesome_group, subparsers)

Making a release
----------------

The tools follow the SemVer versioning scheme. It is important to remember
that whenever the module version is bumped, the version in the docs must be set
to the same value.
