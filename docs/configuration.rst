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

    # Location of SR spending.git
    # (if set to null, then this setting is ignored)
    spending: null
