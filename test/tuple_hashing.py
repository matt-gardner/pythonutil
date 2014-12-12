#!/usr/bin/env python

from datetime import datetime
from random import Random

def main():
    r = Random()
    tuple_labels = dict()
    long_labels = dict()
    keys = set()
    print 'Loading file'
    filename = '/home/mg1/data/graphchi/nell_642_rels_cats/labeled_edges.tsv'
    for line in open(filename):
        source, target, relation = line.strip().split('\t')
        source = int(source)
        target = int(target)
        tuple_labels[(source, target)] = relation
        long_labels[int_pair_to_long(source, target)] = relation
    print 'Starting tuple lookup test'
    start = datetime.now()
    for i in range(3000000):
        s = r.randint(0,1000000)
        t = r.randint(0,1000000)
        label = tuple_labels.get((s,t), None)
    end = datetime.now()
    delta = end - start
    print 'Tuple lookup took', delta.seconds + delta.microseconds / 1000000.0,
    print 'seconds'
    print 'Starting long lookup test'
    start = datetime.now()
    for i in range(3000000):
        s = r.randint(0,1000000)
        t = r.randint(0,1000000)
        label = long_labels.get(int_pair_to_long(s,t), None)
    end = datetime.now()
    delta = end - start
    print 'Long lookup took', delta.seconds + delta.microseconds / 1000000.0,
    print 'seconds'



def int_pair_to_long(first, second):
    return (first << 32) | (second & 0xFFFFFFFFL)


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
