#!/usr/bin/env python

from __future__ import division

def entropy(dist):
    """Finds the entropy of a categorical distribution (with a natural log).

    dist is assumed to be a list, where each entry in the list is a probability
    value; i.e., sum(dist) = 1."""
    from math import log
    return sum(-x*log(x) for x in dist)


def h_index(dist):
    """Finds the h-index of a categorical distribution.

    dist is assumed to be a list, where each entry in the list is a probability
    value; i.e., sum(dist) = 1.

    The h-index is defined as sum_x p(x)^2.
    """
    return sum(x**2 for x in dist)


def mean(nums):
    return sum(nums) / float(len(nums))


def mean_permutation_test(data1, data2, num_samples=None):
    """Performs a permutation test using the mean as the test statistic.

    Both data1 and data2 are assumed to be lists of numerical values.  The
    resultant value is an approximation to the exact p-value, as we use a
    random sampling of permutations instead of enumerating all of them.
    """
    from copy import copy
    from random import Random
    r = Random()
    n = 0
    if not num_samples:
        num_samples = (len(data1) + len(data2)) * 25
    alldata = copy(data1)
    alldata.extend(data2)
    true_diff = abs(mean(data1) - mean(data2))
    num_a = len(data1)
    for i in xrange(num_samples):
        r.shuffle(alldata)
        diff = abs(mean(alldata[num_a:]) - mean(alldata[:num_a]))
        if diff > true_diff:
            n += 1
    return n/num_samples


def paired_permutation_test(data1, data2, weights=None):
    """Performs an exact a paired permutation test.

    We create an array of the signed difference between the two data points,
    find the mean difference, and then test for all possible permutations of
    the signs if the new mean difference is higher than the original mean
    difference.
    """
    if len(data1) != len(data2):
        raise ValueError('This is a _paired_ test and you gave me data with'
                ' unequal lengths!')
    if weights and len(weights) != len(data1):
        raise ValueError("You passed weights that don't match the data")
    from itertools import izip
    diffs = [x-y for x,y in izip(data1, data2)]
    if weights:
        total_weight = sum(weights)
        for i in range(len(diffs)):
            diffs[i] = diffs[i] * weights[i] / total_weight
    length = len(diffs)
    mean_diff = abs(sum(diffs)/length)
    n = 0
    for i in range(2**len(diffs)):
        a = i
        index = 1
        diff = 0
        while index <= length:
            if a%2 == 1:
                diff -= diffs[-index]
            else:
                diff += diffs[-index]
            if a > 0:
                a = a>>1
            index += 1
        diff = abs(diff/length)
        if diff >= mean_diff:
            n += 1
    return n/2**len(diffs)



# vim: et sw=4 sts=4
