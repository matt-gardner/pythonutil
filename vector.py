#!/usr/bin/env python

from __future__ import division
import math

class Vector(object):
    """A simple vector object with some basic functionality, for when you just
    need to do some simple math that isn't very computationally intensive.  If
    you need a really fast vector class, this isn't it; use something like
    numpy instead."""

    def __init__(self, values):
        self.values = values
        if type(self.values[0]) != float:
            self.values = [float(x) for x in self.values]

    def dot(self, other):
        return sum(x * y for x, y in zip(self.values, other.values))

    def norm(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        norm = self.norm()
        if norm == 0: return
        self.values = [x / norm for x in self.values]

    def add(self, other):
        newValues = [x + y for x, y in zip(self.values, other.values)]
        return Vector(newValues)


# vim: et sw=4 sts=4
