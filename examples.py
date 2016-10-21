#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 17:54:54 2016-10-21

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""


import kdtree
import knn
import math

dist = []
# Manhattan distance
dist.append(lambda a, b: sum(
    abs(a[axis] - b[axis])**2 for axis in range(len(a))))
# Euclidean distance
dist.append(lambda a, b: math.sqrt(
    sum(abs(a[axis] - b[axis])**2 for axis in range(len(a)))))


def example_kdtree():
    # An example of how to use kdtree
    print "*"*60
    print "*"*15, "An Example of kdtree's Usage", "*"*15
    print "*"*60
    point1 = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (8, 8)]
    print "point list"
    print point1
    # Create a kdtree
    root = kdtree.create(point1, dimensions=2)
    # Visualize the kdtree
    print "visualize the kd-tree: "
    kdtree.visualize(root)
    # Search for k-nearsest neighbor
    ans = root.search_knn(point=(7, 3), k=3, dist=dist[0])
    print "The 3 nearest nodes to point (7, 3) are:"
    print ans
    print "The nearest node to the point is:"
    print ans[0][0].data


def example_knn():
    # An example of how to use knn
    print "*"*60
    print "*"*16, "An Example of knn's Usage", "*"*17
    print "*"*60
    data = [((3, 5), 1), ((2, 3), 1), ((5, 4), 1), ((9, 6), 0),
            ((4, 7), 1), ((8, 1), 0), ((7, 2), 1), ((8, 8), 0)]
    m = knn.KNN(data, dimensions=2)
    print "Samples:", m.train_data
    print "\nLabel prb:", m.class_prb
    # print m.decision()
    print "\n\nvisualize the kd-tree: "
    m.visualize_kdtree()
    print "the label of point", (9, 9), "is",
    print m.classify(point=(9, 9), k=3, dist=None)
    print "the label of point", (2, 8), "is",
    print m.classify(point=(2, 8), k=3, dist=dist[1], prbout=1)
    knn.saveknn(m, 'testknn.pkl')

    # Pickle test
    print "*"*60
    print "Load knn model from file: 'testknn.pkl'"
    n = knn.loadknn('testknn.pkl')
    print "Samples:", n.train_data
    print "\nLabel prb:", n.class_prb
    # print n.decision()
    print "\n\nvisualize the kd-tree: "
    n.visualize_kdtree()


if __name__ == "__main__":
    example_kdtree()
    example_knn()
