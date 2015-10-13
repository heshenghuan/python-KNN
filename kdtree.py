# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:40:30 2015

@author: heshenghuan
"""
from __future__ import print_function

import math
import operator
from functools import wraps
from collections import deque

# maps child position to its comparison operator
# 0: search left child, means searching in decreasing direction
# 1: search right child, means searching in increasing direction
COMPARE_CHILD = {
    0: (operator.le, operator.sub),
    1: (operator.ge, operator.add),
}

def require_axis(f):
    """ Check if the object of the function has axis and sel_axis members """
    @wraps(f)
    def _wrapper(self, *args, **kwargs):
        if None in (self.axis, self.sel_axis):
            raise ValueError('%(func_name) requires the node %(node)s '
                    'to have an axis and a sel_axis function' %
                    dict(func_name=f.__name__, node=repr(self)))

        return f(self, *args, **kwargs)

    return _wrapper

class KDNode:
    """
    A Node that contains kd-tree specific data and methods. 
    """
    def __init__(self, data=None, parent=None, left=None, right=None, axis=None, 
            sel_axis=None, dimensions=None):
        """
        Creates a new node for a kd-tree.

        If the node will be used within a tree, the axis and the sel_axis
        function should be supplied.

        parent == None, only when the node is the root node.

        sel_axis(axis) is used when creating subnodes of the current node. It
        receives the axis of the parent node and returns the axis of the child
        node.
        """
        # Node.__init__(self, data, parent, left, right)
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
        self.axis = axis
        self.sel_axis = sel_axis
        self.dimensions = dimensions

    def is_leaf(self):
        """
        Returns True if a Node has no subnodes.

        Note that if Node has no data, returns True.
        """
        return (not self.data) or (all(not bool(c) for c, p in self.children))

    def children(self):
        """
        Returns an iterator for the children of the Node.

        The children are returnd as (Node, pos) tuples where pos is 0 for the
        left subnode and 1 for the right subnode.
        """
        if self.left and self.left.data is not None:
            yield self.left, 0
        if self.right and self.right.data is not None:
            yield self.right, 1

    # def set_child(self, index, child):
    #     """
    #     Sets one of the node's children, index 0 refers to the left, 1 to the 
    #     right.
    #     """
    #     if index == 0:
    #         self.left = child
    #     else:
    #         self.right = child

    # def set_parent(self, parent=None):
    #     """
    #     Sets the parent node of node.
    #     """
    #     self.parent = parent

    def height(self):
        """Returns height of the (sub)tree."""
        # If self is not None, it's height should be at least 1
        min_height = int(bool(self))
        return max([min_height]+[c.height()+1 for c, p in self.children()])

    def get_child_pos(self, child):
        """
        Returns the position of the given child.
        
        If the given child is the left child, returns 0. The right child, 1 is returned.
        Otherwise None.
        """
        for c,p in self.children:
            if child == c:
                return p

    @require_axis
    def add(self, point):
        """
        Adds a point to the current node or iteratively descends to one
        of its children.
        """
        current = self
        while True:
            check_dimensionality([point], dimensions=current.dimensions)

            # Adding has hit an empty leaf-node, add here
            if current.data is None:
                current.data = point
                return current

            # split on self.axis, recurse either left or right
            if point[current.axis] < current.data[current.axis]:
                if current.left is None:
                    current.left = current.create_subnode(point)
                    return current.left
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = current.create_subnode(point)
                    return current.right
                else:
                    current = current.right

    @require_axis
    def create_subnode(self, data):
        return self.__class__(data,parent=self,
                axis=self.sel_axis(self.axis),
                sel_axis=self.sel_axis,
                dimensions=self.dimensions)

    def should_remove(self, point, node):
        """ checks if self's point (and maybe identity) matches """
        if not self.data == point:
            return False
        
        return (node is None) or (node is self)
    
    @require_axis
    def remove(self, point, node=None):
        """
        Removes the node with the given point from the tree

        Returns the new root node of the (sub)tree.

        If there are multiple points matching "point", only one is removed. The
        optional "node" parameter is used for checking the identity, once the
        removeal candidate is decided.
        """
        # Recursion has reached an empty leaf node, nothing here to delete
        if not self:
            return

        # Recursion has reached the node should to be delete
        if self.should_remove(point, node):
            return self._remove(point)

        # Remove direct subnode
        if self.left and self.left.should_remove(point, node):
            self.left = self.left._remove(point)
        elif self.right and self.right.should_remove(point, node):
            self.right = self.right._remove(point)

        # Recurse to subtrees
        if point[self.axis] <= self.data[self.axis]:
            if self.left:
                self.left = self.left.remove(point, node)
        if point[self.axis] >= self.data[self.axis]:
            if self.right:
                self.right = self.right.remove(point, node)
        return self

    @require_axis
    def find_replacement(self):
        """ 
        Finds a replacement for the current node.In kd-tree, the replacement 
        node should be the most right node at left subtree, or the most left
        node at right subtree.

        The replacement is returned as a
        (replacement-node, replacements-parent-node) tuple.
        """

        if self.right:
            child, parent = self.right.extreme_child(min, self.axis)
        else:
            child, parent = self.left.extreme_child(max, self.axis)

        return (child, parent if parent is not None else self)

    def extreme_child(self, sel_func, axis):
        """
        Returns a child of the subtree and its parent

        The child is selected by sel_func which is either min or max
        (or a different function with similar semantics). 
        """

        max_key = lambda child_parent: child_parent[0].data[axis]

        # we don't know our parent, so we include None
        me = [(self, None)] if self else []

        child_max = [c.extreme_child(sel_func, axis) for c, _ in self.children]
        # insert self for unknown parents
        child_max = [(c, p if p is not None else self) for c, p in child_max]

        candidates =  me + child_max

        if not candidates:
            return None, None

        return sel_func(candidates, key=max_key)

    @require_axis
    def _remove(self, point):
        # deleting a leaf node is trivial
        if self.is_leaf:
            self.data = None
            return self

        # We have to delete a non-leaf node here
        # Find a replacement for the node (will be the new subtree-root)
        root, max_p = self.find_replacement()

        # self and root swap positions
        tmp_l, tmp_r = self.left, self.right
        self.left, self.right = root.left, root.right
        root.left, root.right = tmp_l if tmp_l is not root else self, tmp_r if tmp_r is not root else self

        self.axis, root.axis = root.axis, self.axis

        # Special-case if we have not chosen a direct child as the replacement
        if max_p is not self:
            pos = max_p.get_child_pos(root)
            max_p.set_child(pos, self)
            max_p.remove(point, self)
        else:
            root.remove(point, self)
        return root

    def axis_dist(self, point, axis):
        """
        Returns the squared distance at the given axis between the current
        Node and the given point.
        """
        return math.pow(self.data[axis] - point[axis],2)

    def dist(self, point):
        """
        Returns the squared distance between the current Node and the given
        point.
        """
        r = range(len(self.data))
        return sum([self.axis_dist(point, i) for i in r])

    def _search_node(self, point, k, results, examined, get_dist):
        """
        k is the number of nearest neighbors of point.

        results is an ordered dict, while the key-value pair is (node, distance).

        examined is a set.

        get_dist is a distance function, expecting two points and returning a
        distance value. Distance values can be any compareable type.
        """
        examined.add(self)

        # Get current best
        if not results:
            # results is empty
            bestNode = None
            bestDist = float('inf')
        else:
            # find the nearest (node, distance) tuple
            bestNode, bestDist = sorted(results.items(), key=lambda n_d: n_d[1], reverse=False)[0]

        nodesChanged = False

        # If the current node is closer than the current best, then it becomes
        # the current best. And the maximum distance nodes should be removed.
        nodeDist = get_dist(self)
        if nodeDist < bestDist:
            if len(results) == k and bestNode:
                # results.pop(bestNode)
                # here is the difference, i remove the max dist node
                maxNode, maxDist = sorted(results.items(), key=lambda n: n[1], reverse=True)[0]
                results.pop(maxNode)

            results[self] = nodeDist
            nodesChanged = True
        # If we're equal to the current best, add it, regardless of k
        elif nodeDist == bestDist:
            results[self] = nodeDist
            nodesChanged = True
        # If we don't have k results yet, add it anyway
        elif len(results) < k:
            results[self] = nodeDist
            nodesChanged = True

        # Get new best only if nodes have changed
        if nodesChanged:
            bestNode, bestDist = sorted(results.items(), key=lambda n: n[1], reverse=False)[0]

        # Check whether there could be any points on the other side of the splitting
        # hyperplane that are closer to the search point than the current best.
        for child, pos in self.children():
            if child in examined:
                continue

            examined.add(child)
            compare, combine = COMPARE_CHILD[pos]

            # Since the hyperplanes are all axis-aligned this is implemented
            # as a simple comparison to see whether the difference between the
            # splitting coordinate of the search point and current node is less
            # than the distance (overall coordinates) from the search point to
            # the current best.
            nodePoint = self.data[self.axis]
            pointPlusDist = combine(point[self.axis], bestDist)
            lineIntersects = compare(pointPlusDist, nodePoint)

            # If the hypersphere crosses the plane, there could be nearer
            # points on the other side of the plane, so the algorithm must move
            # down the other branch of the tree from the current node looking
            # for closer points, following the same recursive process as the
            # entire search.
            if lineIntersects:
                child._search_node(point, k, results, examined, get_dist)

    def search_knn(self, point, k, dist=None):
        """
        Returns the k nearest neighbors of the given point and their distance.

        point must be an actual point in same dimensions, not a node.

        k is the number of results to return. The actual results can be less 
        (if there aren't more nodes to return) or more in case of equal 
        distance.

        dist is a distance function, expecting two points and returning a
        distance value. Distance values can be any compareable type.

        The result is an ordered list of (node,distance) tuples.
        """
        prev = None
        current = self

        if dist is None:
            get_dist = lambda n: n.dist(point)
        else:
            get_dist = lambda n: dist(n.data, point)

        # go down the trees as we would for inserting
        while current:
            if point[current.axis] < current.data[current.axis]:
                # go to left subtree
                prev = current
                current = current.left
                #print("l,current:",current)
            else:
                # go to right subtree
                prev = current
                current = current.right
                #print("r,current:",current)

        if not prev:
            return []
        # print("prev:",prev)

        examined = set()
        results = {}

        # Go uo the tree, looking for better solutions
        current = prev
        while current:
            print(results)
            current._search_node(point, k, results, examined, get_dist)
            current = current.parent

        return sorted(results.items(), key=lambda a:a[1])

    def __nonzero__(self):
        return self.data is not None
    
    def __repr__(self):
        return "<%(cls)s - %(data)s>"%dict(cls=self.__class__.__name__, data=repr(self.data))    

    __bool__ = __nonzero__

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.data == other
        else:
            return self.data == other.data
    def __hash__(self):
        return id(self)




def create(point_list=None, dimensions=None, axis=0, sel_axis=None,parent=None):
    """ 
    Creates a kd-tree from a list of points

    All points in the list must be of the same dimensionality.

    If no point_list is given, an empty tree is created. The number of
    dimensions has to be given instead.

    If both a point_list and dimensions are given, the numbers must agree.

    Axis is the axis on which the root-node should split.

    sel_axis(axis) is used when creating subnodes of a node. It receives the
    axis of the parent node and returns the axis of the child node.

    parent is the Nodes' parent node. """

    if not point_list and not dimensions:
        raise ValueError('either point_list or dimensions must be provided')

    elif point_list:
        dimensions = check_dimensionality(point_list, dimensions)

    # by default cycle through the axis
    sel_axis = sel_axis or (lambda prev_axis: (prev_axis+1) % dimensions)

    if not point_list:
        return KDNode(sel_axis=sel_axis, axis=axis, dimensions=dimensions)

    # Sort point list and choose median as pivot element
    point_list.sort(key=lambda point: point[axis])
    # print(point_list)
    median = len(point_list) / 2 

    loc   = point_list[median]
    root = KDNode(loc, parent,left=None, right=None, axis=axis, sel_axis=sel_axis)
    root.left  = create(point_list[:median], dimensions, sel_axis(axis),parent=root)
    root.right = create(point_list[median + 1:], dimensions, sel_axis(axis),parent=root)
    #return KDNode(loc, parent=None,left=left, right=right, axis=axis, sel_axis=sel_axis)
    return root


def check_dimensionality(point_list, dimensions=None):
    dimensions = dimensions or len(point_list[0])
    for p in point_list:
        if len(p) != dimensions:
            raise ValueError('All Points in the point_list must have the same dimensionality')

    return dimensions



def level_order(tree, include_all=False):
    """ Returns an iterator over the tree in level-order

    If include_all is set to True, empty parts of the tree are filled
    with dummy entries and the iterator becomes infinite. """

    q = deque()
    q.append(tree)
    while q:
        node = q.popleft()
        yield node

        if include_all or node.left:
            q.append(node.left or node.__class__())

        if include_all or node.right:
            q.append(node.right or node.__class__())



def visualize(tree, max_level=100, node_width=10, left_padding=5):
    """ Prints the tree to stdout """

    height = min(max_level, tree.height()-1)
    max_width = pow(2, height)

    per_level = 1
    in_level  = 0
    level     = 0

    for node in level_order(tree, include_all=True):

        if in_level == 0:
            print()
            print()
            print(' '*left_padding, end=' ')

        width = int(max_width*node_width/per_level)

        node_str = (str(node.data) if node else '').center(width)
        print(node_str, end=' ') 

        in_level += 1

        if in_level == per_level:
            in_level   = 0
            per_level *= 2
            level     += 1

        if level > height:
            break

    print()
    print()

# if __name__ == "__main__":
#     point1 = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
#     root = create(point1,dimensions=2)
#     #print(root)
#     print("point list")
#     print(point1)
#     print("visualize the kd-tree: ")
#     visualize(root)
#     ans = root.search_knn(point=(7,3),k=2,dist=None)
#     print (ans)