budget-query
============

Synopsis
--------

``sr budget-query [-h] {total,hist} <subtree_path>``

Description
-----------

Run a query on a specific subtree of the budget.

You should run this from your ``budget.git`` clone.

Options
-------

--help, -h
    Display help and exit.

total
    Calculate the total budget for the subtree and display it.

hist
    Calculate the totals for the subtree items and display it as a histogram
    in a graphical window.

Examples
--------

.. code::

    $ sr budget-query total sr2015
    Total: £24865.24
    $
