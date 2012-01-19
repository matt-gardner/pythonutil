#!/usr/bin/env python

from __future__ import division
from copy import copy
from numpy import mean
from random import Random


def mean_permutation_test(data1, data2, num_samples=None):
    """Perform a permutation test using the mean as the test statistic.

    Both data1 and data2 are assumed to be a list of numerical values.  The
    resultant value is an approximation to the exact p-value, as we use a
    random sampling of permutations instead of enumerating all of them.
    """
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


# vim: et sw=4 sts=4
