budget-diff
===========

Show differences between the budget on various git commits.

.. code::

    Usage: budget-diff [-h] [--tree] [--limit LIMIT] [--zero-hide] old [new]

``old`` and ``new`` are valid Git references.

Example
-------

.. code::

    $ sr budget-diff --tree HEAD~2
