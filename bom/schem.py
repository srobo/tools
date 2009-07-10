"""Routines for extracting information from schematics"""
import eagle

EAGLE = 0
UNKNOWN = 1

def schem_type(fname):
    """Returns the type of file.
    At the moment it'll return EAGLE or UNKNOWN."""
    f = open( fname, "r" )

    if eagle.file_is_eagle(f):
        return EAGLE

    return UNKNOWN

def open_schem(fname):
    s = schem_type(fname)
    if s == EAGLE:
        return eagle.EagleSchem(fname)
    else:
        raise "We don't yet support exporting BOMs from non-EAGLE things"

