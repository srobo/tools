from __future__ import print_function, division
import argparse
from datetime import timedelta
from math import ceil, floor

def nop(*args, **kwargs):
    pass

def parse_time_hours(x):
    hours, minutes = x.split(':')
    return timedelta(hours=int(hours), minutes=int(minutes))

def command(args):
    vprint = print if args.verbose else nop
    slots = int(floor(args.time.total_seconds() / (60*args.match_length)))
    vprint('{} slots'.format(slots))

    entrants_per_slot = args.arenas * args.entrants
    slots_required_for_allvsall = int(ceil(args.teams / entrants_per_slot))
    vprint('{} slots required for an all vs all'.format(slots_required_for_allvsall))

    rounds = int(floor(slots / slots_required_for_allvsall))
    print('{} matches per team (rounds)'.format(rounds))
    time_between_matches_seconds = args.time.total_seconds() / (rounds + 1)
    print('Average time between matches: {}'.format(timedelta(seconds=time_between_matches_seconds)))

    float_periods = slots - (rounds * slots_required_for_allvsall)
    vprint('Float time: {} ({} match periods)'.format(timedelta(minutes=float_periods*args.match_length), float_periods))

def add_subparser(subparsers):
    parser = subparsers.add_parser('comp-calculate-league-matches',
                                   help='Calculate team appearances in an SR league')
    parser.add_argument('--arenas',
                        type=int,
                        default=1,
                        help='number of arenas')
    parser.add_argument('--time',
                        type=parse_time_hours,
                        required=True,
                        help='total league time')
    parser.add_argument('--teams',
                        type=int,
                        required=True,
                        help='number of participating teams')
    parser.add_argument('--entrants',
                        type=int,
                        default=4,
                        help='number of entrants into each game')
    parser.add_argument('--match-length',
                        type=int,
                        default=5,
                        help='length of each match period, in minutes')
    parser.add_argument('--verbose',
                        action='store_true',
                        help='verbose output')
    parser.set_defaults(func=command)

