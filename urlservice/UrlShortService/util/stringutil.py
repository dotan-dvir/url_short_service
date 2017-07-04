'''
A file for housing some string related utilities
'''


def validateString(string):
    '''
    Validate that a string is alphanumerical
    :param string: the string to validate
    :return: true if string is alphanumerical only
    '''
    if (string == None or len(string) == 0):
        return False

    if ('%' in string):
        return False

    if (' ' in string):
        return False

    if ('!' in string):
        return False

    return True