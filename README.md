python-KNN
===

####Introducion
> python-KNN is a simple implementation of K nearest
> neighbors algorithm in Python.
> 
> Algorithm used kd-tree as basic data structure.

####Usage of kdtree.py
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
    (<KDNode - (7, 2)>, 1.0), (<KDNode - (8, 1)>, 5.0), (<KDNode - (9, 6)>, 13.0)]
    
