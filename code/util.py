from constants import VALUES_36_10
import random

# NUMBER INCREMENT FUNCTIONS
def _10ToBase36(number):
    """
    Converts a number from base 10 (integer) to base 36 (string).
    
    INPUT:
        int - number: the number that will be converted

    RETURN TYPE:
        str: converted number
    """
    
    output = []                                                         
    
    while number > 0:                                                     
        number, result = divmod(number, 36)                             
        output.append(VALUES_36_10[result])                                     
    
    output.reverse()                                                       
    output = ''.join(output)                                                   

    return output                                                  

def _36ToBase10(number):
    """
    Converts a number from base 36 (string) to base 10 (integer).
    
    INPUT:
        str - number: the number that will be converted

    RETURN TYPE:
        int: converted number
    """
    
    output = 0                                                            
    x = 0

    for char in number:                                                     
        output += VALUES_36_10.index(char) * (36 ** x)                            
        x += 1

    return output                                                           

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

    if level == 5:                                                       
        calculatedSuffix = _36ToBase10(suffix) + children                    
        if calculatedSuffix < 36:                                            
            calculatedSuffix = '00' + str(_10ToBase36(calculatedSuffix))      
        elif calculatedSuffix < 1296:                                       
            calculatedSuffix = '0' + str(_10ToBase36(calculatedSuffix))      
        elif calculatedSuffix < 46656:                                      
            calculatedSuffix = str(_10ToBase36(calculatedSuffix))            
        else:                                                               
            return -1                                                  
    else:                                                               
        calculatedSuffix = '000'                                             

    return calculatedSuffix                                      

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

    if level == 2:                                                        
        toConvert = _36ToBase10(prefix[0]) + children                  
        calculatedPrefix = _10ToBase36(toConvert) + prefix[1] + prefix[2]    
    elif level == 3:                                                 
        toConvert = _36ToBase10(prefix[1]) + children                           
        calculatedPrefix = prefix[0] + _10ToBase36(toConvert) + prefix[2]    
    elif level == 4:                                                          
        toConvert = _36ToBase10(prefix[2]) + children                        
        calculatedPrefix = prefix[0] + prefix[1] + _10ToBase36(toConvert) 
    else:                                                                    
        calculatedPrefix = prefix                                

    return calculatedPrefix                                       

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

    if is_valid(number):                                        
        prefix = number[1:4]                                
        suffix = number[5:]

        newPrefix = increment_prefix(prefix, amount, level)           
        newSuffix = increment_suffix(suffix, amount, level)

        newNumber = '#' + newPrefix + '-' + newSuffix                           

        return newNumber                                          

def is_valid(number):
    """
    Checks if a given number is valid or not.
    
    INPUT:
        str - number: the number to check
    
    RETURN TYPE:
        bool: whether the number is valid or not
    """

    if len(number) != 8: return False                                      

    number = number.replace('#', '')                                        
    number = number.replace('-', '')
        
    for x in number:                                                       
        if x not in VALUES_36_10: return False                      

    return True                                                  

def calc_hash(parent_number, self_number):
    """
    Calculates a number to hash the components.

    INPUT:
        int - parent_number: the hash number of the parent
        str - self_number: the string number of the current component

    RETURN TYPE:
        int: the calculated hash number 
    """
    
    if not parent_number:
        parent_number = 0
        
    self_number = self_number.replace('#', '')
    self_number = self_number.replace('-', '')
    self_number = _36ToBase10(self_number) * 36 ** 2

    parent_number = int(parent_number)

    output_hash = (parent_number + self_number + random.randint(0, 99999999)) % 10007

    return output_hash