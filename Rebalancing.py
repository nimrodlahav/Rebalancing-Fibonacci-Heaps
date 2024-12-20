#id1: 205541170
#name1: nimrod lahav
#username1: nimrodlahav
#id2:
#name2:
#username2:

"""A class representing a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 
    
    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return False


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.root = None

    """searches for a node in the dictionary corresponding to the key (starting at the root)
    
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode, int)
    @returns: a tuple (x, e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        curr = self.root
        path = 1 # Initialize path
        while curr != None and curr.key != key:
            if curr.key > key:
                curr = curr.left
            else: # The desired node is located in the left subtree
                curr = curr.right
            path += 1
        if curr != None:
            return curr, path
        else: # AVL tree does not contain a node with the key k
            return curr, -1

    """searches for a node in the dictionary corresponding to the key, starting at the max
    
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode, int)
    @returns: a tuple (x, e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        curr = self.max_node()
        path = 1 # Initialize path
        while curr != self.root and curr.parent.key > key:
            curr = curr.parent
            path += 1
        while curr != None and curr.key != key:
            if curr.key > key:
                curr = curr.left
            else: # The desired node is located in the left subtree
                curr = curr.right
            path += 1
        if curr != None:
            return curr, path
        else: # AVL tree does not contain a node with the key k
            return curr, -1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode, int, int)
    @returns: a 3-tuple (x, e, h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, val):
    new_node = AVLNode(key,val)
    depth = search(key)[1]
    parent = search(key)[0].parent     
    new_node.parent = parent            # insertion
    new_node.height = 0                 # adjust new node's height

    while parent != null:
        prev_height = parent.height
        parent.height = 1 + max(parent.left.height, parent.right.height)

        BF_parent = new_node.parent.left.height - new_node.parent.right.height
        if abs(BF_parent)<2 and prev_height == parent.height:
            return                                                  # balanced
        elif abs(BF_parent)<2 and prev_height != parent.height:
            parent = parent.parent
            continue
        elif abs(BF_parent) == 2:       # rotation required
            if BF_parent == 2:
                if parent.left.height-parent.right.height == 1:     # right rotation
                    parent.right = parent.parent
                    parent.parent.left = parent.right

                    parent.parent = 
                    
                
                    parent.parent = pointer1
                    parent.right = pointer2
                    pointer
                    
                    
                else:           # left then right rotation

            else:   # BF_parent=-2
                if parent.left.height-parent.right.height == -1     # left rotation
                    parent.right.left = parent
                else:       # right then left rotation            
                    parent.right.left, parent
        return None, -1, -1

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode, int, int)
    @returns: a 3-tuple (x, e, h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def finger_insert(self, key, val):
        return None, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        return	

    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separating self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """

    def rebalancePostInsertion(self, p):
        while p != None:
            prevHeight = p.height
            if abs(p.getBF()) < 2 and prevHeight == p.setHeight():  # Terminal case: Height has not changed
                break
            elif abs(p.getBF()) < 2 and prevHeight != p.setHeight():  # Promotion case: P's height has changed
                p = p.parent
            else:  # Terminal case: Rotation
                if p.getBF() == 2:
                    if p.left.getBF() == 1:  # Single Right Rotation
                        self.rightRotation(p.left)
                    elif p.left.getBF() == -1:  # Left then right rotation
                        self.leftRotation(p.left.right)
                        self.rightRotation(p.left)
                else:  # p.getBF() == -2
                    if p.right.getBF() == 1:  # Right then left rotation
                        self.rightRotation(p.right.left)
                        self.leftRotation(p.right)
                    elif p.right.getBF() in [-1, 0]:  # Single left rotation
                        self.leftRotation(p.right)
                break

    def rebalancePostDeletion(self, p):
        while p != None:
            prevHeight = p.height
            if abs(p.getBF()) < 2 and prevHeight == p.setHeight():  # Terminal case: Height has not changed
                break
            elif abs(p.getBF()) < 2 and prevHeight != p.setHeight():  # Promotion case: P's height has changed
                p = p.parent
            else:  # Promotion case: Rotation
                if p.getBF() == 2:
                    if p.left.getBF() in [1, 0]:  # Single right rotation
                        self.rightRotation(p.left)
                    elif p.left.getBF() == -1:  # Left then right rotation
                        self.leftRotation(p.left.right)
                        self.rightRotation(p.left)
                else:  # p.getBF() == -2
                    if p.right.getBF() == 1:  # Right then left rotation
                        self.rightRotation(p.right.left)
                        self.leftRotation(p.right)
                    elif p.right.getBF() in [-1, 0]:  # Single left rotation
                        self.leftRotation(p.right)
                p = p.parent

    def rightRotation(self, p):
        p.parent.left = p.right
        if p.parent.parent.left == p.parent:
            p.right = p.parent.parent.left
            p.parent.parent.left = p
        else:
            p.right = p.parent.parent.right
            p.parent.parent.right = p
        p.parent = p.parent.parent
        p.right.parent = p
        p.right.setHeight()

    def leftRotation(self, p):
        p.parent.right = p.left
        if p.parent.parent.left == p.parent:
            p.left = p.parent.parent.left
            p.parent.parent.left = p
        else:
            p.left = p.parent.parent.right
            p.parent.parent.right = p
        p.parent = p.parent.parent
        p.left.parent = p
        p.left.setHeight()

    def getBF(self, v):
        return v.right.height - v.left.height

    def setHeight(self, p):
        # Virtual node's height is -1
        left_height = p.left.height if p.left else -1  
        right_height = p.right.height if p.right else -1  
        p.height = max(p.right.height, p.left.height) + 1   
        
    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    def split(self, node):
        return None, None

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of tuples (key, value) representing the data structure
    """
    def avl_to_array(self):
        return None

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        curr = self.root
        while curr.right != null:
            curr = curr.right
        return curr        

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return -1	

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return None
