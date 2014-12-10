from __future__ import print_function

import hashlib
import os
import re
import subprocess

from sr.tools.environment import get_cache_dir


def file_is_geda_pcb(f):
    """Return true if the file is a gEDA PCB file."""
    f.seek(0)

    # 'PCB[' will occur at the start of one of the first 20 or so lines
    for i in range(20):
        if re.search(r"^\s*PCB[ \t]*\[", f.readline()) is not None:
            return True
    return False


class GSchem(dict):
    """
    Reads in gEDA file.

    :param str fname: The filename of the schematic.
    """
    def __init__(self, fname):
        """Create a new gEDA schematic object."""
        self.fname = fname
        self.__load_bom()

    def __export_bom(self, ofname):
        command = 'gnetlist -g partslist1 -o %s %s' % (ofname, self.fname)
        subprocess.check_call(command, shell=True)

    def __load_bom(self):
        cache_dir = get_cache_dir('bom', 'geda', 'bom')

        ab = os.path.abspath(self.fname)

        # Generate cache filename
        h = hashlib.sha1()
        h.update(ab.encode('UTF-8'))
        cfname = os.path.join(cache_dir, h.hexdigest())

        cache_good = False
        if os.path.exists(cfname):
            # Discover if the cache is still valid
            schem_t = os.path.getmtime(ab)
            cache_t = os.path.getmtime(cfname)

            if cache_t > schem_t:
                # Cache is good
                cache_good = True

        if not cache_good:
            self.__export_bom(cfname)
        else:
            print("Using cached BOM for %s." % os.path.basename(self.fname))

        self.__parse_bom_fname(cfname)

    def __parse_bom_fname(self, fname):
        f = open(fname, "r")

        # Skip the first two lines
        f.readline()
        f.readline()

        for line in f:
            if line[0] == ".":
                "Ignore lines beginning with '.'"
                continue

            fields = line.split()

            value = fields[2].strip().lower()
            id = fields[0].strip().upper()

            self[id] = value

        f.close()


class PCB:
    """
    Read in a gEDA PCB file.

    :param str fname: The filename of the PCB file.
    """
    def __init__(self, fname):
        """Create a new PCB object."""
        self.fname = fname

    def __export_image(self, res, ofname):
        cmd = 'pcb -x png --as-shown --layer-stack "outline,component,silk" ' \
              '--dpi {dpi} --outfile {outfile} {filename}'
        p = subprocess.Popen(cmd.format(dpi=res, outfile=ofname,
                                        filename=self.fname), shell=True)
        p.communicate()
        p.wait()

    def __export_xy(self, ofname):
        p = subprocess.Popen("""pcb -x bom --xyfile %s %s""" %
                             (ofname, self.fname), shell=True)
        p.communicate()
        p.wait()

    def get_image(self, res):
        """
        Get an image of the PCB.

        :returns: The contents of the image.
        """
        cache_dir = get_cache_dir('bom', 'geda', 'pcbimg')

        ab = os.path.abspath(self.fname)

        # Generate cache filename
        h = hashlib.sha1()
        h.update(ab + str(res))
        cfname = os.path.join(cache_dir, h.hexdigest())

        cache_good = False
        if os.path.exists(cfname):
            img_t = os.path.getmtime(ab)
            cache_t = os.path.getmtime(cfname)

            if cache_t > img_t:
                cache_good = True

        if not cache_good:
            self.__export_image(res, cfname)
        else:
            print('Using cached PCB image for %s.' %
                  os.path.basename(self.fname))

        with open(cfname) as file:
            img = file.read()
        return img

    def get_xy(self):
        """
        Get XY file for the PCB.

        :returns: The XY file contents.
        """
        cache_dir = get_cache_dir('bom', 'geda', 'pcbxy')

        ab = os.path.abspath(self.fname)

        # Generate cache filename
        h = hashlib.sha1()
        h.update(ab)
        cfname = os.path.join(cache_dir, h.hexdigest())

        cache_good = False
        if os.path.exists(cfname):
            xy_t = os.path.getmtime(ab)
            cache_t = os.path.getmtime(cfname)

            if cache_t > xy_t:
                cache_good = True

        if not cache_good:
            self.__export_xy(cfname)
        else:
            print("Using cached PCB xy-data for %s" %
                  os.path.basename(self.fname))

        f = open(cfname, "r")
        xy = f.read()
        f.close()
        return xy
