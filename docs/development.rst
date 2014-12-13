Development
===========

Here are some instructions to aid development of the tools.

Adding New Tools
----------------

Adding a new tool is a fairly straightforward process.

You need to create a file in the ``sr/tools/cli`` directory with a filename
that vaguely resembles the name used to invoke the command. For example, if
your command was ``kill-all-the-humans``, you would have the filename as
``kill_all_the_humans.py``.

In that file you should create two functions. The first one, typically called
``command``, will be invoked when the user requests your command to run. It
should accept a single :py:class:`argparse.Namespace` instance which is the
result from the argument parsing.

The second function should be called ``add_subparser`` and should accept an
``argparse`` subparser object. The function should then set up any subparsers
for the command to run. It is important that somewhere in that function you set
the default value in the argument parser of ``func`` to the command function
you create first. An empty command file would look something like this:

.. code::

    def command(args):
        if not args.quiet:
            print(args)


    def add_subparser(subparsers):
        parser = subparsers.add_parser('print-args')
        parser.add_argument('--quiet', '-q', action='store_true', dest='quiet')
        parser.set_defaults(func=command)

Finally, you should make sure to include the new file in the ``__all__`` list
of the ``__init__.py`` file in ``sr/tools/cli``.

It would be a good idea when the tool is finished to write some documentation
for it. You can achieve this by creating a new file in the ``docs/commands``
directory and writing a reStructuredText file, following the template of the
others. This will be automatically picked up and turned into a man page.

Exception Handling
------------------

The command runner will catch many common exceptions and display a nice error
message to the user. The list of exceptions explicitly delt with is:

- ``ImportError``
- ``NotAnInventoryError``

Good Practices
--------------

Since individual commands are Python modules, it is a good idea to use deferred
module loading as much as possible. This not only speeds up loading of the
``sr`` command but also means all the commands won't break if a single one
expects an obscure module.

Making a Release
----------------

The tools should generally follow `Semantic Versioning <http://semver.org/>`_.

.. warning:: It is important to remember that whenever the module version is
             bumped, the version in the docs is also changed to the same
             version.
