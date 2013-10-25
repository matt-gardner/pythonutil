#!/usr/bin/env python


def read_dict_from_tsv(filename, separator='\t', dict_class=dict):
    d = dict_class()
    for line in open(filename):
        key, value = line.strip().split(separator)
        d[key] = value
    return d


def read_list_from_file(filename):
    l = []
    for line in open(filename):
        l.append(line.strip())
    return l


def read_list_of_lists_from_tsv(filename, separator='\t'):
    l = []
    for line in open(filename):
        l.append(line.strip().split(separator))
    return l

# vim: et sw=4 sts=4
