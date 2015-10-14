python-KNN
===

####Introducion
> python-KNN is a simple implementation of K nearest
> neighbors algorithm in Python.
> 
> Algorithm used kd-tree as basic data structure.

###Usage of kdtree.py
----
	>>> import kdtree
	
	# the point list
	>>> point = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
	
	# create a kdtree using point as data
	>>> root = kdtree.create(point,dimensions=2)
	
	# visualize
	>>> print("point list")
    >>> print(point1)
    point list
	[(2, 3), (4, 7), (5, 4), (7, 2), (8, 1), (9, 6)]
    
    >>> print("visualize the kd-tree: ")
    >>> kdtree.visualize(root)
    visualize the kd-tree: 


                       (7, 2)                  

             (5, 4)               (9, 6)        

        (2, 3)     (4, 7)     (8, 1)
    
    # search for k nearest neighbors
    >>> ans = root.search_knn(point=(7,3),k=2,dist=None)
    >>> print (ans)
    [(<KDNode - (7, 2)>, 1.0), (<KDNode - (8, 1)>, 5.0)]
    
    >>> ans = root.search_knn(point=(7,3),k=3,dist=None)
    >>> print (ans)
    [(<KDNode - (7, 2)>, 1.0), (<KDNode - (8, 1)>, 5.0), (<KDNode - (9, 6)>, 13.0)]
    
    
    
###Usage of knn.py
> You can read the code in the knn.py

----

	>>> data = [((3,5),1),((2, 3), 1), ((5, 4), 1), ((9, 6), 0), ((4, 7), 1), ((8, 1), 0), ((7, 2), 1), ((8, 8), 0)]
    >>> m = KNN(data,dimensions=2)
    >>> print "Samples:",m.train_data
    Samples: {(5, 4): 1, (8, 1): 0, (4, 7): 1, (8, 8): 0, (2, 3): 1, (9, 6): 0, (7, 2): 1, (3, 5): 1}
    
    >>> print "\nLabel prb:",m.class_prb
    Label prb: {0: 0.4, 1: 0.6}
    
    >>> print "\n\nvisualize the kd-tree: "
    >>> m.visualize_kdtree()
    visualize the kd-tree:


                                           (7, 2)

                       (3, 5)                                   (9, 6)

             (5, 4)               (4, 7)               (8, 1)               (8, 8)

        (2, 3)


    # Manhattan distance
    >>> f = lambda a, b: sum( abs(a[axis]-b[axis]) for axis in range(len(a)))     
    
    # Using Euclidean distance
    >>>print "the label of point",(9,9),"is",m.classify(point=(9,9),k=3,dist=None)
    the label of point (9, 9) is 0
    
    # Using Manhattan distance
    >>>print "the label of point",(2,8),"is",m.classify(point=(2,8),k=3,dist=f)
	the label of point (2, 8) is 1

