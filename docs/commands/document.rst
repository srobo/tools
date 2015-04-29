document
========

Synopsis
--------

``sr document [-h] -o <file> [-l] [-s <signature>] [-H] <file>``

Description
-----------

Create an SR branded document.

Options
-------

--help, -h
    Display help and exit.

--output <file>, -o <file>
    The path to the output file.

-l
    Emit LaTeX source rather than a PDF.

-s <signature>
    Add an area in the document for a signature.

-H
    Take HTML input rather than Markdown.

Examples
--------

.. code::

    $ sr document -o README.pdf README.md
