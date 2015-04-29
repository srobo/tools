budget-tree
===========

Synopsis
--------

``sr budget-tree [-h] <path>``

Description
-----------

Draw an ASCII tree of the budget.

You should run this from your ``budget.git`` clone.

Options
-------

--help, -h
    Display help and exit.

Examples
--------

.. code::

    $ sr budget-tree sr2015/kickstart
    --kickstart (558.31)
      |--misc-bits (100.00)
       --shipping (458.31)
         |--overseas (260.00)
         |--pallets (15.00)
         |--packing (34.97)
         +--courier (148.34)
    $
