#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 14:22:09 2016-10-22

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import math

# Manhattan distance
ManhattanDistance = (lambda a, b: sum(
    abs(a.get(axis, 0.) - b.get(axis, 0.)) for axis in range(len(a))))
# Euclidean distance
EuclideanDistance = (lambda a, b: math.sqrt(
    sum(abs(a.get(axis, 0.) - b.get(axis, 0.))**2 for axis in range(len(a)))))
# Chebyshev distance
ChebyshevDistance = (lambda a, b: max(
    abs(a.get(axis, 0.) - b.get(axis, 0.)) for axis in range(len(a))))


def MinkowskiDistance(p=1):
    """
    Minkowski distance.

    Given a lambda function by value p.
    """
    if p == 1:
        return ManhattanDistance
    elif p == 2:
        return EuclideanDistance
    elif p == float('INF'):
        return ChebyshevDistance
    elif p == float('-INF'):
        return lambda a, b: min(
            abs(a.get(axis, 0.) - b.get(axis, 0.)) for axis in range(len(a)))
    else:
        return lambda a, b: sum(abs(a.get(axis, 0.) - b.get(axis, 0.))**p
                                for axis in range(len(a)))**(1.0 / p)
