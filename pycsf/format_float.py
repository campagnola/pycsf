import numpy as np


def formatFloat(x, precision=3):
    """Default formatting for displaying float values.
    
    * Chooses number of decimal places based on desired precision
    * Removes superfluous trailing zeros and decimal point
    * Does not use scientific notation.
    """
    if x == 0:
        return '0'
    xstr = str(x)
    if 'nan' in xstr or 'inf' in xstr:
        return xstr
    order = int(np.floor(np.log10(abs(x)))) + 1
    decimals = max(0, precision - order)
    xstr = str(round(x, decimals))
    parts = xstr.partition('.')
    if parts[1] == '':
        return parts[0]
    dec_part = parts[2][:decimals].rstrip('0')
    if dec_part == '':
        return parts[0]
    return parts[0] + '.' + dec_part
