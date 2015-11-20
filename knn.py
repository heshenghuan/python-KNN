# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 23:45:21 2015

@author: heshenghuan
"""

import kdtree


class KNN:
    """
    A KNN Model that contains a kdtree build by specific data, and it can do
    some classification tasks.
    """

    def __init__(self, train_data=None, dimensions=None, axis=0,
                 sel_axis=None):
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
        self.train_data = dict(train_data)
        self.labels = set(self.train_data.values())
        self.class_prb = self._calc_train_class_prb(self.train_data.values())
        self.kdtree = kdtree.create(
            self.train_data.keys(), dimensions, axis, sel_axis)

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
                prb[self.train_data[kdnode.data]] += 1
            for label in self.labels:
                prb[label] = prb[label] / n
            return sorted(prb.items(), key=lambda n: n[1], reverse=True)

    def classify(self, point=None, k=1, dist=None):
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
        """
        if not point:
            return []

        neighbors = self.kdtree.search_knn(point, k, dist)
        prb = self.decision(neighbors)
        # print prb
        return prb[0][0]

    def visualize_kdtree(self):
        """
        Visualize the kdtree.
        """
        kdtree.visualize(self.kdtree)

if __name__ == "__main__":
    data = [((3, 5), 1), ((2, 3), 1), ((5, 4), 1), ((9, 6), 0),
            ((4, 7), 1), ((8, 1), 0), ((7, 2), 1), ((8, 8), 0)]
    m = KNN(data, dimensions=2)
    print "Samples:", m.train_data
    print "\nLabel prb:", m.class_prb
    # print m.decision()
    print "\n\nvisualize the kd-tree: "
    m.visualize_kdtree()
    f = lambda a, b: sum(abs(a[axis] - b[axis])
                         for axis in range(len(a)))  # Manhattan distance
    print "the label of point", (9, 9), "is",
    print m.classify(point=(9, 9), k=3, dist=None)
    print "the label of point", (2, 8), "is",
    print m.classify(point=(2, 8), k=3, dist=f)
