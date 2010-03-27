#!/usr/bin/env python

def split_name(name):
    if 'Other' in name:
        return 'Other','','Other',''
    # For suffixes like Jr. and Sr.
    tmp = name.split(', ')
    if len(tmp) == 1:
        suffix = '_'
    else:
        suffix = tmp[1]
    # Names are separated by spaces, generally
    names = tmp[0].split(' ')
    firstname = names[0]
    lastname = names[-1]
    # A person could have two or more middle names, or just one
    middlename = ' '.join(names[1:-1])
    if middlename == '':
        middlename = '_'
    # If middlename and suffix are empty, '_' will be returned, for use in
    # databases (which is why this was first written)
    return firstname, middlename, lastname, suffix

def remove_titles(name):
    newname = name.replace('Elder ','')
    newname = newname.replace('President ','')
    newname = newname.replace('Bishop ','')
    newname = newname.replace('Sister ','')
    return newname

# vim: et sw=4 sts=4
