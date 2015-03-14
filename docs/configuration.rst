Configuration
=============

The tools are configurable using a YAML file found in ``~/.sr/config.yaml``.

The configuration file looks something like this:

.. code-block:: yaml

    # Student Robotics username
    user: null

    # Store passwords in the keyring if it's available
    use_keyring: False

    # The keyring to store passwords in if keyring use is enabled:
    keyring_service: "SR tools"

    # The SR server
    server: www.studentrobotics.org
    # The port to access HTTPS on
    https_port: 443

    # ssh URL for git to use with gerrit
    gerrit_ssh: "sr-gerrit"

    # Location of SR spending.git
    # (if set to null, then this setting is ignored)
    spending: null

To clone from gerrit, you will need to set up an ssh key and an ssh config file.

The config file should be found in ``~/.ssh/config``. If it doesn't already exist, create it.

It should contain this:

.. code-block::
        
        Host studentrobotics.org
	        User username

        Host sr-gerrit
	        Hostname studentrobotics.org
	        User username
	        Port 29418

To create an ssh key, type ``ssh-keygen``. You will then need to upload the **public** part of the key to http://srobo.org/gerrit.

By default this is stored in ``~/.ssh/id_rsa.pub``.
