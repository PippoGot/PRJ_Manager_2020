from constants import VALUES_36_10 as values

# NUMBER INCREMENT FUNCTIONS
def _10ToBase36(number):
    """
    Converts a number from base 10 (integer) to base 36 (string).
    
    INPUT:
        int - number: the number that will be converted

    RETURN TYPE:
        str: converted number
    """
    
    output = []                                                                 # list for the output string
    
    while number > 0:                                                           # while the number is greater than 0
        number, result = divmod(number, 36)                                     # the number is divided by 36 and both the result and the rest are stored
        output.append(values[result])                                           # the corresponding value is extracted from the dictionary and added to the output string
    
    output.reverse()                                                            # the string characters order is reversed
    output = ''.join(output)                                                    # and the string is concatenated

    return output                                                               # and returned

def _36ToBase10(number):
    """
    Converts a number from base 36 (string) to base 10 (integer).
    
    INPUT:
        str - number: the number that will be converted

    RETURN TYPE:
        int: converted number
    """
    
    output = 0                                                                  # initialise an output number at 0
    x = 0

    for char in number:                                                         # for every character of the string passed as argument
        output += values.index(char) * (36 ** x)                                # the output number is incremented by the corresponding value multiplied by the weight of it's position
        x += 1

    return output                                                               # and the number is returned

def increment_suffix(suffix, children, level):
    """
    Increment the number passed as argument based on the other two arguments.
    
    INPUT:
        str - suffix: the number to be incremented
        int - children: value to add to the number to increment
        int - level: value to decide how to increment the number

    RETURN TYPE:
        str: the incremented number
    """

    if level == 5:                                                              # if the level is 5 (leaf node)
        calculatedSuffix = _36ToBase10(suffix) + children                       # converts the number passed as argument and adds children
        if calculatedSuffix < 36:                                               # if the number is less than 36 (Z + 1)base36
            calculatedSuffix = '00' + str(_10ToBase36(calculatedSuffix))        # the number has 1 digit, so two zeroes are added to the converted number
        elif calculatedSuffix < 1296:                                           # if the number is less than 1296 (ZZ + 1)base36
            calculatedSuffix = '0' + str(_10ToBase36(calculatedSuffix))         # the number has 2 digits so one zero will be added to the converted number
        elif calculatedSuffix < 46656:                                          # if the number is less than di 46656 (ZZZ + 1)dase36
            calculatedSuffix = str(_10ToBase36(calculatedSuffix))               # the number has 3 digits and is converted
        else:                                                                   # finally if none of the previous cases is met
            return -1                                                           # -1 is returned
    else:                                                                       # if level is not 5
        calculatedSuffix = '000'                                                # the number is set to default

    return calculatedSuffix                                                     # finally the calculated number is returned

def increment_prefix(prefix, children, level):
    """
    Increment the number passed as argument based on the other two arguments.
    
    INPUT:
        str - prefix: the number to be incremented
        int - children: value to add to the number to increment
        int - level: value to decide how to increment the number

    RETURN TYPE:
        str: the incremented number
    """

    if level == 2:                                                              # if level is  2 (main assembly)
        toConvert = _36ToBase10(prefix[0]) + children                           # the number at the first position is incremented
        calculatedPrefix = _10ToBase36(toConvert) + prefix[1] + prefix[2]       # then the new number is recomposed
    elif level == 3:                                                            # if level is 3 (assembly)
        toConvert = _36ToBase10(prefix[1]) + children                           # the number at the second position is incremented
        calculatedPrefix = prefix[0] + _10ToBase36(toConvert) + prefix[2]       # then the new number is recomposed
    elif level == 4:                                                            # if level is 4 (subassembly)
        toConvert = _36ToBase10(prefix[2]) + children                           # the number at the third position is incremented
        calculatedPrefix = prefix[0] + prefix[1] + _10ToBase36(toConvert)       # then the new number is recomposed
    else:                                                                       # if the level is greater than 4
        calculatedPrefix = prefix                                               # the number remains unchanged

    return calculatedPrefix                                                     # returns the calculated value

def increment_number(number, amount, level):
    """
    Increment the number passed as argument based on the other two arguments.
    
    INPUT:
        str - number: the number to be incremented
        int - amount: value to add to the number to increment
        int - level: value to decide how to increment the number

    RETURN TYPE:
        str: the incremented number
    """

    if is_valid(number):                                                        # if the given number is valid
        prefix = number[1:4]                                                    # extract the prefix from the original number                                                                 # otherwise the remaining part of the number the suffix
        suffix = number[5:]

        newPrefix = increment_prefix(prefix, amount, level)                     # the new values are calculated
        newSuffix = increment_suffix(suffix, amount, level)

        newNumber = '#' + newPrefix + '-' + newSuffix                           # the resulting number is recomposed

        return newNumber                                                        # and returned

def is_valid(number):
    """
    Checks if a given number is valid or not.
    
    INPUT:
        str - number: the number to check
    
    RETURN TYPE:
        bool: whether the number is valid or not
    """

    if len(number) != 8: return False                                           # if the string has 8 characters

    number = number.replace('#', '')                                            # the non number characters # and - are removed
    number = number.replace('-', '')
        
    for x in number:                                                            # then for every remaining character
        if x not in values: return False                                        # check if it is in the values dictionary

    return True                                                                 # if every character is in the dictionary returns True