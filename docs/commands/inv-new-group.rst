inv-new-group
=============

Synopsis
--------

``sr inv-new-asset [-h] [-a] [-e] <template>``

Description
-----------

Create a new group of assets from an assembly template.

Your currently configured Git name and email address must have an entry in the
``.meta/users`` file.

Options
-------

--help, -h
    Display help and exit.

--all, -a
    Create all the elements of the assembly too. This should only be used when
    initially added a whole assembly into the inventory.

--editor, -e
    Open the newly created asset file in your editor.

Examples
--------

.. code::

    $ sr inv-new-group -a -e motor-board-mcv4b-assy
    Created new assembly with name "motor-board-mcv4b-assy-srP1N2D"
    Created new asset with name "motor-board-mcv4b-srP1P2C"
    Created new asset with name "motor-board-mcv4b-case-srP1Q2B"
