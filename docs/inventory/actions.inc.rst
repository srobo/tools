Actions
-------

Creation of Assets
~~~~~~~~~~~~~~~~~~

Assets should be created with the :doc:`../commands/inv-new-asset` command.
This command takes a single argument which is the name of the asset
(i.e. ``motor-board``). The new asset is created by copying a template with the
name of the asset from the ``.meta/parts`` dir in the inventory repository. If
the template does not exist the template ``default`` will be used.

The :doc:`../commands/inv-new-asset` command will generate a new unique asset
code and use this to both name the file and set the ``assetcode`` field in the
file. To create the unique asset code the command requires the user to have a
record in the .meta/users file, this is to ensure there are not collisions
between asset codes. The name looked up in the users file is the git name/email
of the user and the number assigned to a name must be unique. When adding
yourself to the users file please take care to ensure that you do not end up
with the same ID number as another user.

Creation of Assemblies
~~~~~~~~~~~~~~~~~~~~~~

Assemblies are groups of assets which have their own asset code allowing for
the grouping of assets to be tracked over time. An example of an assembly is a
power board which consists of: case, power board, BeagleBoard, LCD. Assemblies
are represented as directories in the inventory repository. A directory is an
assembly if its name includes an asset code and there is a file called info in
the directory. The info file allows for a description of the assembly to be
stored along with a revision number which allows for log messages to be
recorded about the assembly.

Assemblies can be created in one of two ways. An assembly directory can be
created from scratch with the sr inv-new-group command. This will create the
directory and also the associated info file. As with the creation of assets
this command will look for templates for the info file in ``.meta/assemblies``.
If a directory already exists then this can be promoted to an assembly by
running the :doc:`../commands/inv-new-group` command on it. This will append an
asset code and create the info file.

Creating Assemblies and Assets at the same time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The process of creating assets, then creating an assembly and placing them in
it, is modelled on SRs production process: we manufacture individual pieces of
kit and then combine them into assemblies. However, at the end of SR2011 we
have a large set of kits that are assembled but not in the inventory at all. It
is therefore convenient to have a method of creating both an assembly and it's
assets at the same time, to help putting SR2011s kit into the inventory. This
is achieved with the ``--all`` option to sr :doc:`../commands/inv-new-group`.

Movement of Assets
~~~~~~~~~~~~~~~~~~

When an asset is moved from one location to another, e.g. from a persons house
to the vault, the file representing it is moved in the inventory repository
accordingly. When an asset is in the possession of an individual it is up to
that individual as to how detailed they track the movements of the asset. If
they move it between various locations while it is in their possession then
they are not obliged to detail this in the inventory system, however they are
responsible for its safekeeping.

Logging of Non-state Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It will occasionally be necessary to detail information about an asset that is
not purely conveyed by the state stored in its file. In this case detailed
information can be recorded in a commit message associated with the asset file.
To enable a commit to be made, and associated with a specific file, each asset
file contains a revision number field which can be incremented. This field
means that non-null commits can be made. Incrementing that field can be
achieved by using the :doc:`../commands/inv-touch` command.
