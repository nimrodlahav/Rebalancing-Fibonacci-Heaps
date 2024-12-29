# id1: 205541170
# name1: Nimrod Lahav
# username1: Nimrodlahav1
# id2: 212780829
# name2: Shira Shnizik
# username2: Shirashnizik


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key=None, value=None):
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
        return self.left and self.right

    # Node's height setter
    def set_height(self):
        if self.is_real_node():
            self.height = max(self.left.height, self.right.height) + 1

    # Node's BF calculator
    def get_bf(self):
        if self.is_real_node():
            return self.left.height - self.right.height
        else: # Virtual node's BF
            return 0


"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """
    # Default Initialization with a virtual node as root
    def __init__(self, root=AVLNode()):
        self.root = root

    # Helper method that returns the triplet (key, path, parent)
    def inner_search(self, key, finger=False):
        parent = None
        path = 0  # Path initialization
        if not finger:
            curr = self.get_root()
        else:  # Finger search
            curr = self.max_node()
            if curr.is_real_node():
                # Ascend to the first node with a smaller key (or the root)
                while curr is not self.get_root() and curr.parent.key > key:
                    curr = curr.parent
                    path += 1
        # Descend through the tree as usual, for both cases
        while curr.is_real_node():
            if curr.key != key:
                parent = curr
                if curr.key > key:
                    curr = curr.left
                else: # curr.key < key
                    curr = curr.right
                path += 1
            else: # curr.key == key
                break
        if curr.is_real_node():
            return curr, path + 1, parent
        else: # AVL tree does not contain a node with the key k
            return None, path, parent

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode, int)
    @returns: a tuple (x, e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        desired_node = self.inner_search(key)[0]
        path = self.inner_search(key)[1]
        return desired_node, path

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        desired_node = self.inner_search(key)[0]
        path = self.inner_search(key, True)[1]
        return desired_node, path

    # Helper method for rebalancing an AVL tree after insertion
    def rebalance_post_insertion(self, p):
        promotions = 0
        while p is not None:
            prev_height = p.height
            p.set_height()
            if abs(p.get_bf()) < 2 and prev_height == p.height: # Terminal case: Height has not changed
                break
            elif abs(p.get_bf()) < 2 and prev_height != p.height: # Promotion case: P's height has changed
                p = p.parent
                promotions += 1
            else: # Terminal case: Rotation (|BF(p)|=2)
                if p.get_bf() == 2:
                    if p.left.get_bf() == 1: # Single Right Rotation
                        self.right_rotation(p.left)
                    elif p.left.get_bf() == -1: # Left then right rotation
                        self.left_rotation(p.left.right)
                        self.right_rotation(p.left)
                elif p.get_bf() == -2:
                    if p.right.get_bf() == 1: # Right then left rotation
                        self.right_rotation(p.right.left)
                        self.left_rotation(p.right)
                    elif p.right.get_bf() == -1: # Single left rotation
                        self.left_rotation(p.right)
                break
        return promotions

    # Helper method for rebalancing an AVL tree after deletion
    def rebalance_post_deletion(self, p):
        while p is not None:
            prev_height = p.height
            p.set_height()
            if abs(p.get_bf()) < 2 and prev_height == p.height: # Terminal case: Height has not changed
                break
            elif abs(p.get_bf()) < 2 and prev_height != p.height: # Promotion case: P's height has changed
                p = p.parent
            else: # Terminal\Promotion case: Rotation (|BF(p)|=2)
                if p.get_bf() == 2:
                    if p.left.get_bf() in [1, 0]: # Single Right Rotation
                        self.right_rotation(p.left)
                    elif p.left.get_bf() == -1: # Left then right rotation
                        self.left_rotation(p.left.right)
                        self.right_rotation(p.left)
                else:
                    if p.right.get_bf() == 1: # Right then left rotation
                        self.right_rotation(p.right.left)
                        self.left_rotation(p.right)
                    elif p.right.get_bf() in [-1, 0]: # Single left rotation
                        self.left_rotation(p.right)
                p = p.parent

    # Helper method for performing a right rotation
    def right_rotation(self, piv):
        piv.parent.left = piv.right
        piv.right.parent = piv.parent
        piv.right = piv.parent
        piv.parent = piv.parent.parent
        piv.right.parent = piv
        if piv.parent is not None:
            if piv.parent.left == piv.right:
                piv.parent.left = piv
            else: # piv.parent.right == piv.right
                piv.parent.right = piv
        else: # Self has a new root
            self.root = piv
        # Height updates
        piv.right.set_height()
        piv.set_height()

    # Helper method for performing a left rotation
    def left_rotation(self, piv):
        piv.parent.right = piv.left
        piv.left.parent = piv.parent
        piv.left = piv.parent
        piv.parent = piv.parent.parent
        piv.left.parent = piv
        if piv.parent is not None:
            if piv.parent.left == piv.left:
                piv.parent.left = piv
            else: # piv.parent.right == piv.right
                piv.parent.right = piv
        else: # Self has a new root
            self.root = piv
        # Height updates
        piv.left.set_height()
        piv.set_height()

    # Helper method for insert/finger insert
    def inner_insert(self, key, val, finger=False):
        new_node = AVLNode(key, val)
        parent = self.inner_search(key)[2]
        new_node.parent = parent # Set the node's parent
        # Connecting virtual nodes to new node
        new_node.left = AVLNode()
        new_node.right = AVLNode()
        new_node.left.parent = new_node
        new_node.right.parent = new_node
        new_node.set_height()
        if parent is not None: # Set node's parent child
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
        else: # New_node is the tree's root
            self.root = new_node
        # Node's insert path calculating
        if not finger:
            path = self.search(key)[1]
        else:
            path = self.finger_search(key)[1]
        # promotions counting and rebalancing, if necessary
        promotions = self.rebalance_post_insertion(parent)
        return new_node, path, promotions

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, val):
        return self.inner_insert(key, val)

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def finger_insert(self, key, val):
        return self.inner_insert(key, val, True)

    # Helper method for finding tree's minimum node
    def min_node(self):
        curr = self.root
        if self.root.is_real_node():
            while curr.left.is_real_node():
                curr = curr.left
        return curr

    # Helper method for finding node's successor
    def successor(self, node):
        if node.right.is_real_node(): # Go right once, and then left all the way
            right_subtree = AVLTree(node.right)
            return right_subtree.min_node()
        p = node.parent
        # Go up from node until the first turn right
        while p is not None and node == p.right:
            node = p
            p = node.parent
        return p

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        # Case 1: It's a leaf node (no children)
        if not node.left.is_real_node() and not node.right.is_real_node():
            if node.parent is not None:
                if node.key < node.parent.key:  # If it's a left child
                    node.parent.left = AVLNode()
                else:  # If it's a right child
                    node.parent.right = AVLNode()
            else: # If the tree includes only the deleted node, set its root to virtual node
                self.root = AVLNode()

        # Case 2: Deleted node has one child on the right
        elif not node.left.is_real_node():
            if node.parent is not None:
                if node.key < node.parent.key: # If it's a left child
                    node.parent.left = node.right
                else: # If it's a right child
                    node.parent.right = node.right
            else: # If tree's root is the deleted node, set it to node's left child
                self.root = node.right
            node.right.parent = node.parent # Update the parent's reference to the right child

        # Case 3: Deleted node has one child on the left
        elif not node.right.is_real_node():
            if node.parent is not None:
                if node.key < node.parent.key: # If it's a left child
                    node.parent.left = node.left
                else: # If it's a right child
                    node.parent.right = node.left
            else: # If tree's root is the deleted node, set it to node's right child
                self.root = node.left
            node.left.parent = node.parent # Update the parent's reference to the left child

        # Case 4: Deleted node has two children
        else:
            succ = self.successor(node) # Get the successor of the node to be deleted
            if succ.key < succ.parent.key: # Remove the successor from its current position
                succ.parent.left = succ.right
            else:
                succ.parent.right = succ.right
            succ.right.parent = succ.parent # Update the successor's right child parent
            succ.left.parent = None # disconnecting successor's left virtual node
            succ.parent = node.parent # Set the successor's parent to the parent of the deleted node
            if node.parent is not None: # Update parent's reference to the successor
                if node.key < node.parent.key: # If it's a left child
                    node.parent.left = succ
                else: # If it's a right child
                    node.parent.right = succ
            else:
                self.root = succ
            # Connecting successor to node's children
            succ.right = node.right
            succ.left = node.left
            succ.right.parent = succ
            succ.left.parent = succ

        # Before completely disconnecting the deleted node from the tree, save its parent
        parent = node.parent
        node.parent = None

        # After structural changes, rebalance the tree if necessary
        self.rebalance_post_deletion(parent)

    # Helper method that returns tree's height and maximum key
    def tree_height_and_max(self):
        if self.size() == 0:
            return -1, float('-inf')
        else:
            return self.get_root().height, self.max_node().key

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
    def join(self, tree2, key, val):
        join_node = AVLNode(key, val)
        self_height = self.tree_height_and_max()[0]
        tree2_height = tree2.tree_height_and_max()[0]
        if self_height > tree2_height: # Self is higher
            higher_tree = self
            lower_tree = tree2
        else: # Tree2 is higher/both heights are equal
            higher_tree = tree2
            lower_tree = self
        higher_tree_max = higher_tree.tree_height_and_max()[1]
        lower_tree_max = lower_tree.tree_height_and_max()[1]
        curr = higher_tree.get_root()

        if higher_tree_max > lower_tree_max: # Higher tree is on the right
            # Search for node with a height less than or equal to lower tree's height
            while curr.height > max(lower_tree.tree_height_and_max()[0], 0):
                curr = curr.left
            left_root = lower_tree.get_root()
            # Join both trees
            join_node.right = curr
            join_node.parent = curr.parent
            curr.parent = join_node
            if join_node.parent is not None:
                join_node.parent.left = join_node
            join_node.left = left_root
            left_root.parent = join_node
            join_node.set_height()
            higher_tree.rebalance_post_insertion(join_node.parent) # Rebalance, if necessary
        elif higher_tree_max < lower_tree_max: # Higher tree is on the left
            while curr.height > max(lower_tree.tree_height_and_max()[0], 0):
                curr = curr.right
            right_root = lower_tree.get_root()
            # Join both trees
            join_node.left = curr
            join_node.parent = curr.parent
            curr.parent = join_node
            if join_node.parent is not None:
                join_node.parent.right = join_node
            join_node.right = right_root
            right_root.parent = join_node
            join_node.set_height()
            higher_tree.rebalance_post_insertion(join_node.parent) # Rebalance, if necessary

        # If new root does not belong to self, set self's root
        if self_height == -1 or tree2_height == -1 or self_height == tree2_height:
            self.root = join_node
        elif higher_tree == tree2:
            self.root = tree2.get_root()

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
        left_subtree = AVLTree(node.left)
        right_subtree = AVLTree(node.right)
        while node.parent is not None:
            if node.parent.right == node: # Perform join operation on the left subtree
                tree_to_join = AVLTree(node.parent.left)
                left_subtree.join(tree_to_join, node.parent.key, node.parent.value)
            else: # Perform join operation on the right subtree
                tree_to_join = AVLTree(node.parent.right)
                right_subtree.join(tree_to_join, node.parent.key, node.parent.value)
            node = node.parent
        return left_subtree, right_subtree

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of tuples (key, value) representing the data structure
    """
    def avl_to_array(self):
        def avl_to_array_rec(node, in_order_arr):
            if node.is_real_node():
                avl_to_array_rec(node.left, in_order_arr)
                in_order_arr.append((node.key, node.value))
                avl_to_array_rec(node.right, in_order_arr)
            return in_order_arr
        return avl_to_array_rec(self.get_root(), [])

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        curr = self.root
        if self.root.is_real_node():
            while curr.right.is_real_node():
                curr = curr.right
        return curr

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return len(self.avl_to_array())

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

