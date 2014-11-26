budget-query
============

Query the

.. code::

    Usage: sr budget-query CMD SUBTREE_PATH

The ``CMD`` can be one of:

 * ``hist`` displays a histogram of the items in the tree.
 * ``total`` calculates the total cost of the items in the tree.

Examples
--------

.. code::

    $ sr budget-query hist sr2014/competition
    $ sr budget-query total sr2014
