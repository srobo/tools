budget-check
============

Synopsis
--------

``sr budget-check [-h] [-s <spending>]``

Description
-----------

Checks that the budget is in a valid state and prints the result to standard
output.

You should run this from your ``budget.git`` clone.

You may optionaly specify the location of your ``spending.git`` clone for a
more detailed result. If this is not specified, the command will first try and
use the location specified in your configuration. If a suitable location for
``spending.git`` cannot be found, the checks on it will not be performed.

Options
-------

--help, -h
    Display help and exit.

--spending, -s
    Specify the location of the ``spending.git`` clone explicitly.

Examples
--------

.. code::

    $ sr budget-check
    OK: Budget is £1.40412 below maximum.
    OK: All spending.git budget line references are valid.
    OK: No open budget lines are overspent.
    $
