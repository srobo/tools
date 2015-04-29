budget-diff
===========

Synopsis
--------

``sr budget-diff [-h] [--tree] [--limit <limit>] [--zero-hide] old [new]``

Description
-----------

Displays the difference between two ``budget.git`` commits.

You should run this from your ``budget.git`` clone.

You can specify ``old`` and ``new`` using Git-like syntax for specifying a
commit.

Options
-------

--help, -h
    Display help and exit.

--tree, -t
    Display the difference as a tree.

--limit <limit>, -l <limit>
    Limit the output to a specific subtree.

--zero-hide
    Hide lines that have been added or removed with a value of 0.

Examples
--------

.. code::

    $ sr budget-diff -l sr2015/kickstart -t HEAD~4
    --sr (7.21)
       --sr2015 (7.21)
          --kickstart (7.21)
             --shipping (7.21)
               +--packing (7.21)
    $
