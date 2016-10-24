# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 23:45:21 2015

@author: heshenghuan
"""

import kdtree
import dill
from pickle import dump
from pickle import load


class KNN:
    """
    A KNN Model that contains a kdtree build by specific data, and it can do
    some classification tasks.
    """

    def __init__(self, train_data=None, train_label=None, dimensions=None,
                 axis=0, sel_axis=None):
        """
        Creates a new KNN model contains a kdtree build by the point_list.

        train_data is the list of (point, label) tuples, which is sample.
        We use point to build kdtree, and use label to make the decision
        when classify new data.

        All points in the point_list must be of the same dimensionality.
        dimensions is the dimension of points in pointlist.

        If both a point_list and dimensions are given, the numbers must agree.

        axis is the axis on which the root-node should split.

        sel_axis is a function, sel_axis(axis) is used when creating subnodes
        of a node. It receives the axis of the parent node and returns the axis
        of the child node.
        """
        # As train_data is a list of samples, we use dict() to change data
        # structure of samples.
        self.train_data = train_data
        self.train_label = train_label
        self.labels = set(self.train_label)
        self.class_prb = self._calc_train_class_prb(self.train_label)
        self.kdtree = kdtree.create(
            self.train_data, dimensions, axis, sel_axis)

    def _calc_train_class_prb(self, labels_list=None):
        """
        Calculates the probability of each labels in training data.

        Using Laplace Smoothing tech to avoid 0 probability.
        """
        if not labels_list:
            return {}

        n = len(labels_list)
        label_num = len(self.labels)
        prb = {}
        for l in self.labels:
            # tmp = (l, sum(1 if v == l else 0 for k, v in train_data)/n)
            prb[l] = (labels_list.count(l) + 1.0) / (n + label_num)
        return prb

    def decision(self, neighbors=None):
        """
        Using majority voting rule to decided class_label of group neighbors.

        Returns an ordered list of (label, probability) tuples,
        key=probability.

        When neighbors is None, returns self.class_prb.
        """
        if not neighbors:
            return sorted(self.class_prb.items(), key=lambda n: n[1],
                          reverse=True)

        else:
            n = len(neighbors)
            prb = {}
            for label in self.labels:
                prb[label] = 0.0
            for kdnode, dist in neighbors:
                index = self.train_data.index(kdnode.data)
                prb[self.train_label[index]] += 1
            for label in self.labels:
                prb[label] = prb[label] / n
            return sorted(prb.items(), key=lambda n: n[1], reverse=True)

    def classify(self, point=None, k=1, dist=None, prbout=0):
        """
        Classify the point.

        If point is None, returns [].

        k is the number of results to return. The actual results can be less
        (if there aren't more nodes to return) or more in case of equal
        distance.

        dist is a distance function, expecting two points and returning a
        distance value. Distance values can be any compareable type.

        By default dist will be the KDNode.dist(), which is the Euclidean
        distance.
        If you want to change the method of distance calculation, for example,
        you can set like following:

        dist = lambda a, b: sum(abs(a[axis]-b[axis]) for axis in range(len(a)))

        for calculating Manhattan distance.

        prbout: 0 just return the class.
                1 return a vec of probability of each class.
        """
        if not point:
            return []

        neighbors = self.kdtree.search_knn(point, k, dist)
        prb = self.decision(neighbors)
        # print prb
        if prbout == 0:
            return prb[0][0]
        elif prbout == 1:
            return prb

    def visualize_kdtree(self):
        """
        Visualize the kdtree.
        """
        kdtree.visualize(self.kdtree)


def saveknn(knn_model, outfile):
    out = open(outfile, 'w')
    # Pickle the knn_model using the highest protocol available.
    dump(knn_model, out, -1)
    out.close()


def loadknn(srcfile):
    src = open(srcfile, 'r')
    knn_model = load(src)
    src.close()
    return knn_model
