#!/usr/bin/env python
from __future__ import division
from numpy import zeros, array
from evilplot import Plot, Points

def main():
    #do_k_means('iris.cluster.txt')
    #do_k_means('balance-test.cluster.txt')
    print
    do_iris_HAC()
    print
    #do_balance_HAC()

def do_k_means(filename):
    numvars, names, data, labels = read_data(filename)
    bestk, minerror, K = k_means_best_k(data, 2)
    for cluster in K.clusters:
        print cluster.indices
    print bestk, minerror

def do_iris_HAC():
    numvars, names, data, labels = read_data('iris.cluster.txt')
    DE = HAC(data, .1)
    data = []
    for grouping in DE:
        if grouping[0] != 0:
            K = grouping[2]
            K.compute_means()
            data.append((grouping[1], K.error()))
            print grouping[0], grouping[1], K.error()
            for cluster in K.clusters:
                cluster.indices.sort()
                print cluster.indices
    plot = Plot()
    plot.title = 'SSE as a function of number of clusters in HAC'
    plot.append(Points(data, style='lines'))
    plot.write('hac_clusters.gpi')

def do_balance_HAC():
    numvars, names, data, labels = read_data('balance-train.cluster.txt')
    DE = HAC(data, 1, 0)
    for grouping in DE:
        if grouping[0] != 0:
            print grouping[0], grouping[1], grouping[2].error()

def make_matrix(data, n=2):
    matrix = zeros((len(data),len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            matrix[i,j] = norm(data[i],data[j], n)
    return matrix

def make_binary_matrix(adj_matrix, d):
    new_matrix = zeros(adj_matrix.shape)
    len, wid = adj_matrix.shape
    for i in range(len):
        for j in range(wid):
            if adj_matrix[i,j] <= d:
                new_matrix[i,j] = 1
    return new_matrix

def HAC(data, step, base=0, n=2):
    adj_matrix = make_matrix(data, n)
    d = base
    k = len(data)
    K = []
    for datum in data:
        c = Cluster(datum)
        K.append(c)
    DE = []
    DE.append((d, k, K))

    while k != 1:
        oldk = k
        d = d + step
        a = make_binary_matrix(adj_matrix, d)
        k, newK = new_clusters(a, data)
        if oldk != k:
            DE.append((d, k, newK))
    return DE

def new_clusters(adj_matrix, data):
    K = Cluster_Set()
    width, height = adj_matrix.shape
    for i in range(width):
        if K.contains_index(i)[0]:
            #print 'Found cluster with',i
            c = K.contains_index(i)[1]
        else:
            #print 'Making new cluster for',i
            c = Cluster()
            K.add_cluster(c)
        for j in range(height):
            if adj_matrix[i,j] and not c.contains_index(j):
                if K.contains_index(j)[0]:
                    #print 'Detected duplicate cluster.  Fixing it...'
                    oldcluster = K.contains_index(j)[1]
                    for index in c.indices:
                        if not oldcluster.contains_index(index):
                            oldcluster.add(data[index],index)
                    K.remove_cluster()
                    c = oldcluster
                #print 'Adding',j,'to cluster with',i
                c.add(data[j], j)
    return K.num_clusters(), K

def k_means_best_k(data, normval=2):
    minerror = 10000000
    bestk = 0
    bestclusters = None
    for i in range(2,8):
        clusters, error = k_means(data, i, normval)
        if error < minerror:
            bestclusters = clusters
            minerror = error
            bestk = i
        print i, error
    return bestk, minerror, bestclusters

def k_means(data, k, normval=2):
    means = []
    K = Cluster_Set()
    for i in xrange(k):
        K.add_cluster(Cluster(data[i]))

    clusters = K.clusters
    while not K.is_finished():
        for i in xrange(k):
            clusters[i].reset()
        for index, datum in enumerate(data):
            closest = 0
            dist = norm(datum, clusters[closest].mean, normval)
            for i in range(len(clusters)):
                if (norm(datum, clusters[i].mean, normval) < dist):
                    dist = norm(datum, clusters[i].mean, normval)
                    closest = i
            clusters[closest].add(datum, index)
        K.compute_means()
    return K, K.error()

class Cluster:
    def __init__(self, datum=None):
        self.oldmean = []
        self.mean = []
        if datum is not None:
            self.oldmean = [0,]*len(datum)
            self.mean = datum
        self.data = []
        self.indices = []

    def add(self, datum, index):
        self.data.append(datum)
        self.indices.append(index)

    def reset(self):
        self.data = []
        self.indices = []

    def compute_mean(self):
        self.oldmean = self.mean
        dims = len(self.mean)
        if dims == 0:
            dims = len(self.data[0])
        sum = [0,]*dims
        for datum in self.data:
            for i in range(dims):
                sum[i] += datum [i]
        for i in range(dims):
            sum[i] = sum[i]/len(self.data)
        self.mean = sum

    def is_finished(self):
        return self.oldmean == self.mean

    def error(self):
        e = 0
        if len(self.mean) == 0:
            self.compute_mean()
        for datum in self.data:
            e += norm(datum, self.mean)
        return e

    def contains_item(self, item):
        for dautm in self.data:
            if datum == item:
                return True
        return False

    def contains_index(self, i):
        for index in self.indices:
            if i == index:
                return True
        return False

    def sort_indices(self):
        self.indices.sort()

class Cluster_Set:
    def __init__(self):
        self.clusters = []

    def __iter__(self):
        return iter(self.clusters)

    def __len__(self):
        return len(self.clusters)

    def add_cluster(self, c):
        self.clusters.append(c)

    def contains_item(self, item):
        for c in self.clusters:
            if c.contains_item(item):
                return True, c
        return False, []

    def contains_index(self, i):
        for c in self.clusters:
            if c.contains_index(i):
                return True, c
        return False, []

    def get_cluster(self, i):
        return self.clusters[i]

    def compute_means(self):
        for c in self.clusters:
            c.compute_mean()

    def num_clusters(self):
        return len(self.clusters)

    def is_finished(self):
        for c in self.clusters:
            if not c.is_finished():
                return False
        return True

    def error(self):
        error = 0
        for c in self.clusters:
            error += c.error()
        return error

    def remove_cluster(self):
        self.clusters = self.clusters[:-1]

def norm(x, y, n=2):
    sum = 0
    for i in range(len(x)):
        sum += abs(x[i] - y[i])**n
    return sum**(1/n)

def read_data(filename):
    file = open(filename, 'rU')
    numvars = int(file.readline())
    names = file.readline()[:-1].split(',')
    lines = file.readlines()
    data = []
    labels = []
    for str in lines:
        if str.endswith('\n'):
            str = str[:-1]
        data.append(map(float, str.split(',')[:-1]))
        labels.append(str.split(',')[-1])
    return numvars, names, data, labels

if __name__ == '__main__':
    main()


# vim: et sw=4 sts=4
