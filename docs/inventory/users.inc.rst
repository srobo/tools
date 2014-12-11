Users
-----

New Users
~~~~~~~~~

Before creating or editing assets, you need to record information about
yourself in the inventory. In the file ``.meta/users``, observe a list of users
containing name, email addresse and a unique number. Append your own
information to this list, with the next sequential number following the last
list enry, and using the same email address as for your git commits.

You must ensure that you get this change pushed to the master inventory
repository, ​inventory.git, before creating any assets/assemblies. The users
file is the only part of the system that isn't safe with distributed editing;
if two people add themselves to the users file and create assets without first
getting the users file change pushed things will not end well.
