#!/usr/bin/env python

def assign_to_dict(d, key, value):
    d[key] = value


def append_to_list(d, key, value):
    if key in d:
        l = d[key]
    else:
        l = []
        d[key] = l
    l.append(value)


def extend_list(d, key, value):
    if key in d:
        l = d[key]
    else:
        l = []
        d[key] = l
    l.extend(value)


# The TSV file here must have just two columns.
def read_dict_from_tsv(filename,
                       separator='\t',
                       key_index=0,
                       dict_class=dict,
                       set_function=assign_to_dict,
                       skip_errors=False):
    d = dict_class()
    for line in open(filename):
        try:
            fields = line.strip().split(separator)
            key = fields[key_index]
            if len(fields) == 2:
                value = fields[1 - key_index]
            else:
                if key_index == 0:
                    value = fields[1:]
                else:
                    value = fields[0]
            set_function(d, key, value)
        except IndexError:
            if skip_errors:
                continue
            raise
    return d


# No matter how many columns there are in the TSV file, we treat the first n
# columns as the key, and the rest of the columns as the value.
def read_dict_from_tsv_with_multikey(filename,
                                     num_key_columns,
                                     separator='\t',
                                     dict_class=dict,
                                     aggregator_fn=lambda x, y: y):
    d = dict_class()
    for line in open(filename):
        fields = line.strip().split(separator)
        key = tuple(fields[:num_key_columns])
        value = fields[num_key_columns:]
        try:
            old_value = d[key]
        except ValueError:
            old_value = None
        d.__setitem__(key, aggregator_fn(old_value, value))
    return d


def read_list_from_file(filename):
    l = []
    for line in open(filename):
        l.append(line.strip())
    return l


def read_set_from_file(filename):
    l = set()
    for line in open(filename):
        l.add(line.strip())
    return l


def read_list_of_lists_from_tsv(filename, separator='\t', list_type=list):
    l = []
    for line in open(filename):
        l.append(list_type(line.strip().split(separator)))
    return l


def read_set_of_lists_from_tsv(filename, separator='\t', list_type=list):
    s = set()
    for line in open(filename):
        s.add(list_type(line.strip().split(separator)))
    return s


def create_dirs_and_open(filename):
    """This assumes that you want to open the file for writing.  It doesn't
    make much sense to create directories if you are not going to open for
    writing."""
    try:
        return open(filename, 'w')
    except IOError as e:
        import errno
        if e.errno != errno.ENOENT:
            raise
    directory = filename.rsplit('/', 1)[0]
    try_makedirs(directory)
    return open(filename, 'w')


def try_makedirs(path):
    """Do the equivalent of mkdir -p."""
    import os
    try:
        os.makedirs(path)
    except OSError, e:
        import errno
        if e.errno != errno.EEXIST:
            raise


# vim: et sw=4 sts=4
