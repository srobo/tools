#!/usr/bin/env python
"""Student Robotics inventory system asset code translation library"""
import luhn

# The characters used in asset codes. They have been chosen to avoid similar
# looking characters to avoid errors when reading written codes.
alphabet_lut = ["0", "1", "2", "3", "4", "5", "6", "7",
                "8", "9", "A", "B", "C", "D", "E", "F",
                "G", "H", "J", "K", "L", "M", "N", "P",
                "Q", "R", "T", "U", "V", "W", "X", "Y"]

def num_to_code(uid, pid):
    """Convert a uid/pid number combo to an alphanumeric asset code"""
    uid = int(uid)
    pid = int(pid)
    if uid < 0 or pid < 0:
        raise ValueError("""User/Part ID cannot be negative. UID: %i, PID: %i""" % (uid, pid))

    assetno = ""
    for num in (uid, pid):
        while 1:
            if num > 15:
                r = num % 16
                assetno = assetno + alphabet_lut[r+16]
                num = num/16
            else:
                assetno = assetno + alphabet_lut[num]
                break
    checkdigit = luhn.calc_check_digit(assetno, alphabet_lut)
    assetno = assetno + checkdigit
    assert(luhn.is_valid(assetno, alphabet_lut))
    return assetno
