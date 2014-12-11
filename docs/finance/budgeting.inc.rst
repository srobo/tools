Budgeting
---------

The SR budget is a high-level description of how our money is allocated,
including that which has already been spent.

The budget consists of a hierarchy of entries. Each entry allocates a specified
amount of money to some specified purpose. Each entry contains a description of
what these funds are for, along with some justification for the value of the
entry.

See also :ref:`Purchasing <finance.purchasing>` for a description of how we
operate on the budget.

Embracing Change
~~~~~~~~~~~~~~~~

Our budgeting processes embrace the fact that our plans are going to change.
Unspent budget can be reallocated to new purposes through defined, and
transparent procedures.

The Future and the Past
~~~~~~~~~~~~~~~~~~~~~~~

Our approach to budgeting is somewhat different to the approach that some
people use. Instead of our budget just being a document that at some point in
time was the plan for spending, our budget is always consistent with our
spending plans. Our budget is updated throughout the year: before a spend can
be made, there must be a suitable entry in the budget from which it can be
made.

Furthermore, spent budget entries don't ever disappear. They stay around for
the rest of time. This means that budgeting in the future can be grounded on a
solid base of real data from the past. It also means that our databases of
spends never refer to budget entries that no longer exist.

So, as well as being a plan, the budget is also a historical database.

Implementation
~~~~~~~~~~~~~~

The SR budget is stored as a git repo that contains a collection of .yaml
files. This allows each item to be provided in great detail, and it is
abundantly clear who created what things.

Out income and bank balance at the start of the plan are stored as a couple of
lines in check in the root directory.

Folder Shape
~~~~~~~~~~~~

The ``budget.git`` repo contains individual budget items (or services) in files
whose path describes them. Each folder represents a grouping of things. Thus,
we have:

.. code::

    sr2012/
        clothing.yaml
        competition/
            arena/
            cable-ties.yaml
            prizes.yaml
            trophies.yaml
            etc.
        kickstart/
        kits/
        mentor-travel.yaml
        etc.
    sr2013/
        etc.

File Shape
~~~~~~~~~~

Each of these YAML files must be formed in the same manner, and must have
certain elements. For instance, this is one revision of ``clothing.yaml``:

.. code:: yaml

    summary: T-shirt and other forms of clothing we might buy

    # Cost of the item
    cost: 400

    # Long description
    description: >-
      We spent £480 on t-shirts last year. We still have a few left over so if
      we do get some more this year we won't need as many.

    # Whether the item/service can only be used once
    consumable: false

summary
    This should be a brief summary of the item. Don't include "Cost of", which
    is pointless.

cost
    The cost of the item, including delivery and VAT. Ideally you should find a
    supplier that we can use, and use their normal price for the number we need
    - don't expect that we'll be able to order the item on the special deal
    you've found (but do mention that this is possible in the description).

description
    Detailed description of:
    - The item, including a part code.
    - Why we need it.
    - How you reached the cost you've assigned. You should include links to the
      supplier's website and/or other contact details if they're not a
      web-based company.

consumable
    Whether the item can only be used once. This is mostly aimed at use in the
    budgets that we send to sponsors, but also has value outside this context.
