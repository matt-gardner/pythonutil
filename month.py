#!/usr/bin/env python

def make_month_str(month):
    if month == 1:
        return 'Jan'
    if month == 2:
        return 'Feb'
    if month == 3:
        return 'Mar'
    if month == 4:
        return 'Apr'
    if month == 5:
        return 'May'
    if month == 6:
        return 'Jun'
    if month == 7:
        return 'Jul'
    if month == 8:
        return 'Aug'
    if month == 9:
        return 'Sep'
    if month == 10:
        return 'Oct'
    if month == 11:
        return 'Nov'
    if month == 12:
        return 'Dec'
    raise ValueError('Invalid month!')

def get_month_number(month):
    if 'Jan' in month:
        return 1
    elif 'Feb' in month:
        return 2
    elif 'Mar' in month:
        return 3
    elif 'Apr' in month:
        return 4
    elif 'May' in month:
        return 5
    elif 'Jun' in month:
        return 6
    elif 'Jul' in month:
        return 7
    elif 'Aug' in month:
        return 8
    elif 'Sep' in month:
        return 9
    elif 'Oct' in month:
        return 10
    elif 'Nov' in month:
        return 11
    elif 'Dec' in month:
        return 12
    else:
        raise ValueError("Given string was not a month!")

# vim: et sw=4 sts=4
