# Routines for extracting BOMs from schematics
import subprocess

EAGLE = 0
UNKNOWN = 1

def file_is_eagle(f):
    """Return true if the file is an EAGLE file"""
    f.seek(0)
    b = f.read(2)

    # The first two bytes of eagle files seem to always be 0x10 0x80
    if ord(b[0]) == 0x10 and ord(b[1]) == 0x80:
        return True
    return False

def schem_type(fname):
    """Returns the type of file.
    At the moment it'll return EAGLE or UNKNOWN."""
    f = open( fname, "r" )

    if file_is_eagle(f):
        return EAGLE

    return UNKNOWN

def export_eagle_bom(fname, out_fname):
    p = subprocess.Popen( """sr export_eagle_bom "%s" "%s" """ % (fname, out_fname),
                          shell = True )
    p.communicate()
    p.wait()

def export_bom(fname, ofname):
    s = schem_type(fname)
    if s == EAGLE:
        export_eagle_bom(fname, ofname)
    else:
        raise "We don't yet support exporting BOMs from non-EAGLE things"

