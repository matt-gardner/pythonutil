#!/usr/bin/env python

from stats import paired_permutation_test

def main():
    #data1 = [1,2,3,1,2,3,1,2,3]
    #data2 = [2,2,3,3,2,3,2,2,4]
    data1 = [1,]*10
    data2 = [2,]*10
    p = paired_permutation_test(data1, data2)
    print p


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
