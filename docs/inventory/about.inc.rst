About
-----

In true Student Robotics fashion, the inventory is a Git repository containing
YAML files tied together with Python scripts.

Each asset in the inventory is given a YAML file that could look something like
this:

.. code:: yaml

    assetcode : "000"
    labelled  : false   # Does the asset have its assetcode marked on it
    revision  : 4

    description: >
        A large (6m x 1m) vinyl banner that has the words "STUDENT ROBOTICS" on it
        along with the SR logo and the logos of the motorola foundation, ECS and
        BitBox.

    purchasing_ticket : 0         # The trac ticket number of the purchase request
    value             : 70.00     # A rough estimate of the value of the asset
    condition         : broken   # One of {unknown, working, broken}

    emails:
        - http://groups.google.com/group/srobo/browse_thread/thread/9d83662a2d605455/
        - http://groups.google.com/group/srobo/browse_thread/thread/b47dfdd92b8d2f4c/

    photos:
        - http://www.flickr.com/photos/rspanton/5005242423/
        - http://www.flickr.com/photos/rspanton/4992920951/

This example is in fact taken straight from the inventory, asset 000.
