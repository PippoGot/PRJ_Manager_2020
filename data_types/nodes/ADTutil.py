import re

SPECIAL_PREFIXES = [
    'PRO',
    'MEH',
    'ELH',
    'EMH',
    'MMH',
    'PLC',
    'JIG'
]

# ID UTILITY

def incrementPrefix(prefix, level, quantity):
    """
    Increments a string prefix of the specified amount in a certain way.

    YXX if level = 2;
    XYX if level = 3;
    XXY if level = 4;
    unchanged if level not in [2, 3, 4];

    Args:
        prefix (str): the prefix of the number to increment
        level (int): where the increment should be done
        quantity (int): the amount of increment

    Returns:
        str: the incremented number converted to base 36
    """

    if not 1 < level < 5 or prefix in SPECIAL_PREFIXES:
        return prefix

    if level == 2:
        return toBase36(toBase10(prefix[0]) + quantity) + prefix[1:]

    if level == 3:
        return prefix[0] + toBase36(toBase10(prefix[1]) + quantity) + prefix[2]

    if level == 4:
        return prefix[:2] + toBase36(toBase10(prefix[2]) + quantity)

def incrementSuffix(suffix, level, quantity):
    """
    Increments a string suffix of the specified amount.

    Custom functions:
        toBase36()
        toBase10()

    Args:
        suffix (str): the number to increment
        level (int): where the increment should be done
        quantity (int): the amount to increment the number

    Returns:
        str: the incremented number converted to base 36
    """

    if level > 4:
        suffix = toBase36(toBase10(suffix) + quantity)

    return suffix.zfill(3)

def incrementID(prefix, suffix, level, quantity):
    """
    Increments a complete number and returns it already packed.

    "#XXX-XXX"

    Args:
        prefix (str): the prefix of the number to increment
        suffix (str): the suffix of the number to increment
        level (int): where the increment should be done
        qty (int): the amount to increment the number

    Returns:
        str: the incremented number
    """

    prefix = incrementPrefix(prefix, level, quantity)

    if prefix in SPECIAL_PREFIXES: level = 5

    suffix = incrementSuffix(suffix, level, quantity)

    return packID(prefix, suffix)

def packID(prefix, suffix):
    """
    Composes and returns a number in the wanted format.

    #{prefix}-{suffix};

    Args:
        prefix (str): the first half of the number
        suffix (str): the second half of the number

    Returns:
        str: the formatted number
    """

    return f'#{prefix}-{suffix}'

def unpackID(numberID):
    """
    Removes the non alphanumerical characters from the string and returns the cleaned string.

    Args:
        id (str): the string to clean

    Returns:
        str: the cleaned string
    """

    if numberID:
        numberID = numberID.upper()
        numberID = re.sub(r'[\W_]+', '', numberID)
        return numberID

# CONVERSION

VALUES = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def toBase36(number):
    """
    Converts a number from base 10 to base 36.

    Args:
        number (int): the base 10 number to be converted to base 36

    Returns:
        str: the converted number
    """

    outputCharacters = []

    while number > 0:
        number, rest = divmod(number, 36)
        outputCharacters.append(VALUES[rest])

    outputCharacters.reverse()
    outputCharacters = ''.join(outputCharacters)

    return outputCharacters

def toBase10(string):
    """
    Converts a string to a number from base 36 to base 10.

    Args:
        string (str): the string to convert from base 36 to base 10

    Returns:
        int: the converted number
    """

    output = 0
    x = len(string) - 1

    for char in string:
        output += VALUES.index(char.upper()) * (36 ** x)
        x -= 1

    return output
