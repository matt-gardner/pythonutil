#!/usr/bin/env python

from __future__ import division
from heapq import heappush, heappop

class Index(object):
    def __init__(self):
        self.strings = dict()
        # Confusing, maybe, but I would like this to be 1-indexed, not
        # 0-indexed
        self.array = [-1]
        self.current_index = 1

    def getIndex(self, string, _force_add=False):
        if not _force_add:
            index = self.strings.get(string, None)
            if index:
                return index
        self.strings[string] = self.current_index
        self.array.append(string)
        self.current_index += 1
        return self.current_index - 1

    def getString(self, index):
        return self.array[index]

    def getAllStrings(self):
        return self.array[1:]

    def save_to_file(self, f):
        for i, string in enumerate(self.array):
            if i == 0: continue
            f.write('%d\t%s\n' % (i, string))

    @classmethod
    def read_from_file(cls, f):
        """Initialize an index object from a file.  Assumes file was written by
        the save_to_file method, so the."""
        index = cls()
        if type(f) == str:
            f = open(f)
        for line in f:
            try:
                _, string = line.strip().split('\t')
            except ValueError:
                print 'Offending line:', line
                raise
            index.getIndex(string, _force_add=True)
        return index

# A Counter class.  Basically it's a map with some convenient features.  It's
# based off of a java class written by Dan Klein for the Berkeley NLP group.  I
# didn't implement everything he did - I might later.  Add things as needed.

class Counter:
    def __init__(self):
        self.entries = dict()

    def keySet(self):
        return self.entries.keys()

    def size(self):
        return len(self.entries)

    def isEmpty(self):
        return self.size() == 0

    def containsKey(self, key):
        return key in self.entries

    def getCount(self, key):
        if key not in self.entries:
            return 0
        else:
            return self.entries[key]

    def setCount(self, key, count):
        self.entries[key] = count

    def incrementCount(self, key, inc):
        if key in self.entries:
            self.entries[key] += inc
        else:
            self.entries[key] = inc

    def totalCount(self):
        total = 0
        for key in self.keySet():
            total += self.entries[key]
        return total

    def normalize(self):
        total = self.totalCount()
        for key in self.keySet():
            self.entries[key] = self.entries[key] / total

    def sorted(self):
        heap = []
        for item in self.keySet():
            heappush(heap, (self.getCount(item), item))
        heap.sort()
        heap.reverse()
        return heap


class CounterMap:
    def __init__(self):
        self.map = dict()

    def keySet(self):
        return self.map.keys()

    def setCount(self, key, value, count):
        if key not in self.map:
            self.map[key] = Counter()
        self.map[key].setCount(value, count)

    def incrementCount(self, key, value, count):
        if key not in self.map:
            self.map[key] = Counter()
        self.map[key].incrementCount(value, count)

    def getCount(self, key, value):
        if key not in self.map:
            return 0
        else:
            return self.map[key].getCount(value)

    def getCounter(self, key):
        if key not in self.map:
            self.map[key] = Counter()
        return self.map[key]

    def __getitem__(self, key):
        return self.getCounter(key)

    def totalCount(self):
        total = 0
        for key in self.keySet():
            total += self.map[key].totalCount()
        return total

    def totalSize(self):
        total = 0
        for key in self.keySet():
            total += self.map[key].size()
        return total

    def normalize(self):
        for key in self.keySet():
            self.map[key].normalize()

    def size(self):
        return len(self.map)

    def isEmpty(self):
        return self.size() == 0




# vim: et sw=4 sts=4
