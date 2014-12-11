Technical Details
-----------------

Asset File Format
~~~~~~~~~~~~~~~~~

Each asset is stored as a file with a filename in the form of 'name-assetcode'
where 'name' is the name of the asset e.g. 'battery-charger' and 'assetcode' is
a unique code which can be written on the asset to allow it to be tracked. Each
file is written in YAML and contains information about the asset in pre-defined
fields.

Asset File Fields
~~~~~~~~~~~~~~~~~

A definitive list of file fields can be found in the default template located
in the inventory git repository (``.meta/parts/default``).
