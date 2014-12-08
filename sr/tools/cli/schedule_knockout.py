from __future__ import print_function


def bit_mask(n):
    """Return an n-bit mask of 1's."""
    return 2 ** n - 1


def reverse_bits(n, width):
    """Reverse the bits of n."""
    b = '{:0{width}b}'.format(n, width=width)
    return int(b[::-1], 2)


def command(args):
    import math
    import sys
    import yaml

    # Round the number of teams up to a power of two
    rounded_teams = int(2 ** math.ceil(math.log(args.n_teams, 2)))

    n_per_match = 4
    n_matches = int(math.ceil(float(rounded_teams) / n_per_match))
    matches_bits = int(math.ceil(math.log(n_matches, 2)))

    # Find the order in which we repeatedly insert teams into the
    # match list.
    # The pattern in the insertion offsets is:
    #  - Even offset: Bitwise reversal of the offset in the offset table
    #  -  Odd offset: Complement of the previous number
    # Derived using a similar approach to this website:
    # http://blogs.popart.com/2012/02/things-only-mathematicians-can-get-excited-about/
    # but for matches with 4 teams in.
    ins_order = []
    for n in range(n_matches):
        if n % 2 == 0:
            # Even
            v = reverse_bits(n, matches_bits)
        else:
            # Odd
            v ^= bit_mask(matches_bits)
        ins_order.append(v)

    matches = []
    for n in range(n_matches):
        matches += [[]]

    for n in range(args.n_teams):
        matches[ins_order[n % n_matches]].append(n)

    if args.yaml:
        sys.stdout.write(yaml.dump(matches))
    else:
        for n, match in enumerate(matches):
            print(" {0}:\t{1}".format(n, "\t".join([str(x) for x in match])))


def add_subparser(subparsers):
    parser = subparsers.add_parser('schedule-knockout',
                                   help="Create the schedule for the first "
                                        "round of a knock-out")
    parser.add_argument("n_teams", type=int, help="The number of teams")
    parser.add_argument("--yaml", action="store_true", help="Output YAML")
    parser.set_defaults(func=command)
