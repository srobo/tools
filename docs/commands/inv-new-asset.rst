inv-new-asset
=============

Synopsis
--------

``sr inv-new-asset [-h] [-e] <template>``

Description
-----------

Create a new asset from a template.

Your currently configured Git name and email address must have an entry in the
``.meta/users`` file.

Options
-------

--help, -h
    Display help and exit.

--editor, -e
    Open the newly created asset file in your editor.

Examples
--------

.. code::

    $ sr inv-new-asset led-torch
    Created new asset with name "led-torch-srP1M2E"
