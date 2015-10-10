# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:40:30 2015

@author: heshenghuan
"""

import math

class Node(Object):
	"""
	A Node in a kd-tree. Also, an Binary tree node.
	"""
	def  __init__(self, data=None, left=None, right=None):
		self.data = data
		self.left = left
		self.right = right

	def is_leaf(self):
		"""
		Returns True if a Node has no subnodes
		"""
		return (not self.data) or (all(not bool(c) for c, p in self.children))

	def preorder(self):
		"""Iterator for nodes: root, left, right. """
		if not self:
			return
		# preorder
		yield self
		if self.left:
			for x in self.left.preorder():
				yield x
		if self.right:
			for x in self.right.preorder():
				yield x

	def inorder(self):
		"""Iterator for nodes: left, root, right. """
		if not self:
			return
		
		#inorder
		if self.left:
			for x in self.left.inorder():
				yield x
		yield self
		if self.right:
			for x in self.right.inorder():
				yield x


	def postorder(self):
		"""Iterator for nodes: left, right, root. """
		if not self:
			return
		#postorder
		if self.left:
			for x in self.left.postorder():
				yield x
		if self.right:
			for x in self.right.postorder():
				yield x
		yield self

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

	def set_child(self, index, child):
		"""
		Sets one of the node's children, index 0 refers to the left, 1 to the 
		rigth.
		"""
		if index == 0:
			self.left = child
		else:
			self.rigth = child

	def height(self):
		"""
		Returns height of the (sub)tree.
		"""
		min_height = int(bool(self))
		return max([min_height]+[c.height()+1 for c, p in self.children])

	def get_child_pos(self, child):
		"""Returns the position of the given child.
		If the given child is the left child, returns 0. The right child, 1 is returned.
		Otherwise None.
		"""
		for c,p in self.children:
			if child == c:
				return p


class KDNode(Node):
	"""A Node that contains kd-tree specific data and methods. """
	der __init__(self, data=None, left=None, right=None, axis=None,
			sel_axis=None, dimensions=None):
		"""
		Creates a new node for a kd-tree

        If the node will be used within a tree, the axis and the sel_axis
        function should be supplied.

        sel_axis(axis) is used when creating subnodes of the current node. It
        receives the axis of the parent node and returns the axis of the child
        node. 
		"""
		super(KDNode, self).__init__(data, left, right)
		self.axis = axis
		self.sel_axis = sel_axis
		self.dimensions = dimensions