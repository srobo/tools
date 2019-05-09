"""
A set of functions for dealing with asset codes in the inventory.

Asset codes are constructed from part numbers and user numbers.
"""
from __future__ import division

from sr.tools.inventory import luhn


# The characters used in asset codes. They have been chosen to avoid similar
# looking characters to avoid errors when reading written codes.
ALPHABET = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C",
            "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R",
            "T", "U", "V", "W", "X", "Y"]
ALPHABET_SET = set(ALPHABET)


def normalise(asset_code):
    """
    Normalise the given asset code to one that is compatible with the inventory
    API. Generally this just involves removing the 'sr' from the front and
    making the result all in uppercase.

    :param str asset_code: The asset code to normalise.
    :returns: A normalised part code.
    :rtype: str
    """
    asset_code = asset_code.strip().upper()
    if asset_code.startswith('SR'):
        return asset_code[2:]
    else:
        return asset_code


def is_valid(asset_code):
    """
    Check if an asset code is valid.

    :param str asset_code: The asset code to check.
    :returns: True if valid, else False.
    :rtype: bool
    """
    asset_code = normalise(asset_code)

    invalid_characters = set(asset_code) - ALPHABET_SET
    if invalid_characters:
        return False

    return luhn.is_valid(asset_code, ALPHABET)


def num_to_code(user_number, part_number):
    """
    Convert a user/part number combo to an alphanumeric asset code.

    :param user_number int: The user number.
    :param part_number int: The part number.
    :returns: An asset code string.
    :rtype: str
    """
    if user_number < 0 or part_number < 0:
        raise ValueError('User ({0}) or part ({1}) number cannot be '
                         'negative. '.format(user_number, part_number))

    assetno = ''
    for num in (user_number, part_number):
        while True:
            if num > 15:
                r = num % 16
                assetno = assetno + ALPHABET[r + 16]
                num = num // 16
            else:
                assetno = assetno + ALPHABET[num]
                break

    checkdigit = luhn.calc_check_digit(assetno, ALPHABET)

    assetno = assetno + checkdigit
    assert luhn.is_valid(assetno, ALPHABET)
    return assetno


def code_to_num(asset_code):
    """
    Convert an alphanumeric asset code to a user/part number combo.

    :param str asset_code: The asset code to convert.
    :returns: A tuple consisting of the user and part number.
    :rtype: pair of ints
    """
    asset_code = normalise(asset_code)
    if not is_valid(asset_code):
        raise ValueError("Asset code '{}' is not valid".format(asset_code))

    # Remove checkdigit
    asset_code = asset_code[:-1]

    field = [0, 0]
    fieldno = 0
    i = 0
    for c in asset_code:
        if fieldno == 2:
            raise ValueError("Error in asset code '{}', too many fields"
                             .format(asset_code))
        num = ALPHABET.index(c)
        if num > 15:
            field[fieldno] = field[fieldno] + (num - 16) * (16 ** i)
        else:
            field[fieldno] = field[fieldno] + num * (16 ** i)
            fieldno += 1
            i = -1
        i += 1

    return (field[0], field[1])
