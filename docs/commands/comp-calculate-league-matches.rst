comp-calculate-league-matches
=============================

Synopsis
--------

::


  sr comp-calculate-league-matches [-h] [--arenas ARENAS] --time TIME
                                   --teams TEAMS [--entrants ENTRANTS]
                                   [--match-length MATCH_LENGTH]
                                   [--verbose]

Description
-----------

Calculate the number of matches per team, and the average time between a team's
matches, in a standard SR league structure.

Options
-------

--help, -h
    Display help and exit.

--arenas <arenas>
    The number of arenas in which matches are held in parallel. 1 is assumed if
    not specified.

--time <time>
    The total length of the league, as HH:MM.

--teams <teams>
    The number of teams taking part in the league.

--entrants <entrants>
    The number of entrants into each game. 4 is assumed if not specified.

--match-length <length>
    The length of each match slot, in minutes. 5 is assumed if not specified.

--verbose
    Give more verbose output. Specifically this also gives the total number of
    match periods, the number of match periods required for an all vs all match
    configuration, and the number of unused slots across the league.

Examples
--------

.. code::

    $ sr comp-calculate-league-matches --time 8:45 --teams 54
