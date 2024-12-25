#id1:
#name1: Nimrod Lahav
#username1:
#id2: 212780829
#name2: Shira Shnizik
#username2: Shirashnizik


"""A class represnting a node in an AVL tree"""

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

    def is_real_node(self):
        return self is not None

    # Helper method for calculating node's children height
    def children_height(self):
        left = self.left.height if self.left else -1
        right = self.right.height if self.right else -1
        return left, right

    # Node's height setter
    def set_height(self):
        left_height, right_height = self.children_height()
        self.height = max(left_height, right_height) + 1

    # Helper method for calculating node's Balance Factor
    def get_bf(self):
        left_height, right_height = self.children_height()
        return left_height - right_height

"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self, root=None):
       self.root = root

    # Helper method that returns the triplet (key, path, parent)
    def search_helper(self, key, finger=False):
        if not finger:
            path = 1  # Initialize path
            curr = self.get_root()
            parent = None
        else: # Finger search
            path = 0  # Initialize path
            curr = self.max_node()
            while curr is not self.get_root() and curr.parent.key > key:
                curr = curr.parent
                path += 1
        while curr is not None and curr.key != key:
            parent = curr
            if curr.key > key:
                curr = curr.left
            else: # The desired node is located in the right subtree
                curr = curr.right
            path += 1
        if curr is not None:
            return curr, path, parent
        else: # AVL tree does not contain a node with the key k
            return curr, -1, parent

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode, int)
    @returns: a tuple (x, e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        desired_node = self.search_helper(key)[0]
        path = self.search_helper(key)[1]
        return desired_node, path

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        desired_node = self.search_helper(key)[0]
        path = self.search_helper(key, True)[1]
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
        if piv.right is not None:
            piv.parent.left = piv.right
            piv.right.parent = piv.parent
        piv.right = piv.parent
        piv.parent = piv.parent.parent
        piv.right.parent = piv
        if piv.parent is not None:
            if piv.parent.left == piv.right:
                piv.parent.left = piv
            piv.parent.right = piv
        else:
            self.root = piv
        piv.right.set_height()
        piv.set_height()

    # Helper method for performing a left rotation
    def left_rotation(self, piv):
        if piv.left is not None:
            piv.parent.right = piv.left
            piv.left.parent = piv.parent
        piv.left = piv.parent
        piv.parent = piv.parent.parent
        piv.left.parent = piv
        if piv.parent is not None:
            if piv.parent.left == piv.left:
                piv.parent.left = piv
            piv.parent.right = piv
        else:
            self.root = piv
        piv.left.set_height()
        piv.set_height()

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
        depth = self.search(key)[1] - 1
        new_node = AVLNode(key, val)
        parent = self.search_helper(key)[2]
        new_node.parent = parent
        new_node.set_height()
        if parent is not None:
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
        else: # new_node is the tress's root
            self.root = new_node
        promotions = self.rebalance_post_insertion(parent)
        return new_node, depth, promotions

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
        depth = self.search(key)[1] - 1
        new_node = AVLNode(key, val)
        parent = self.search_helper(key, True)[2]
        new_node.parent = parent
        new_node.set_height()
        if parent is not None:
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
        else:  # new_node is the tress's root
            self.root = new_node
        promotions = self.rebalance_post_insertion(parent)
        return new_node, depth, promotions

    # Helper method for finding the node's successor
    def successor(self, temp):
        temp = self.root
        prev = None
        if temp.right is not None:
            temp = temp.right
            while temp.left is not None:
                temp = temp.left
            prev = temp
        elif temp.left is not None:
            temp = temp.left
            while temp.right is not None:
                temp = temp.right
            prev = temp
        else:
            return None
        return prev.key

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        # Search for the node to delete
        deleted_node = self.search(node.key)[0]

        # Case 1: It's a leaf node (no children)
        if deleted_node.left is None and deleted_node.right is None:
            if node.key < deleted_node.parent.key:  # If it's a left child
                deleted_node.parent.left = None
            else:  # If it's a right child
                deleted_node.parent.right = None

        # Case 2: Deleted node has one child on the right
        elif deleted_node.left is None:
            if node.key < deleted_node.parent.key:  # If it's a left child
                deleted_node.parent.left = deleted_node.right
            else:  # If it's a right child
                deleted_node.parent.right = deleted_node.right
            deleted_node.right.parent = deleted_node.parent  # Update the parent's reference to the right child

        # Case 3: Deleted node has one child on the left
        elif deleted_node.right is None:
            if node.key < deleted_node.parent.key:  # If it's a left child
                deleted_node.parent.left = deleted_node.left
            else:  # If it's a right child
                deleted_node.parent.right = deleted_node.left
            deleted_node.left.parent = deleted_node.parent  # Update the parent's reference to the left child

        # Case 4: Deleted node has two children
        else:
            succ = self.successor(deleted_node)  # Get the successor of the node to be deleted
            succ.parent.left = succ.right  # Remove the successor from its current position
            if succ.right is not None:
                succ.right.parent = succ.parent  # Update the successor's right child parent
            succ.parent = deleted_node.parent  # Set the successor's parent to the parent of the deleted node
            if deleted_node.key < deleted_node.parent.key:  # Update parent's reference to the successor
                deleted_node.parent.left = succ
            else:
                deleted_node.parent.right = succ

        # After structural changes, rebalance the tree if necessary
        self.rebalance_post_deletion(succ.parent)

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

    def tree_high_and_max(self):
        if self.size() == 0:
            return -1, float('-inf')
        else:
            return self.get_root().height, self.max_node().height

    def join(self, tree2, key, val):
        join_node = AVLNode(key, val)
        self_height, self_max = self.tree_high_and_max()[0], self.tree_high_and_max()[1]
        tree2_height, tree2_max = tree2.tree_high_and_max()[0], tree2.tree_high_and_max()[1]
        if self_height > tree2_height:
            higher_tree = self
            lower_tree = tree2
        else:
            higher_tree = tree2
            lower_tree = self
        curr = higher_tree.get_root()
        if self_max > tree2_max:  # Higher tree is on the right
            # Search for node with a height less than or equal to lower tree's height
            while curr.height > lower_tree.get_root().height:
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
            higher_tree.rebalance_post_insertion(join_node.parent)  # Rebalance, if needed
        else:  # Higher tree is on the left
            # Search for node with a height less than or equal to lower tree's height
            while curr.height > lower_tree.get_root().height:
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
            higher_tree.rebalance_post_insertion(join_node.parent)  # Rebalance, if needed

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
        while node is not None:
            if node.parent.right == node:  # Perform join operation on the left subtree
                tree_to_join = AVLTree(node.left)
                left_subtree.join(tree_to_join, node.key, node.value)
            else:  # Perform join operation on the right subtree
                tree_to_join = AVLTree(node.right)
                right_subtree.join(tree_to_join, node.key, node.value)
            node = node.parent
        return left_subtree, right_subtree

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of tuples (key, value) representing the data structure
    """
    def avl_to_array(self):
        def avl_to_array_rec(node, in_order_arr):
            if node is not None:
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
        while curr.right is not None:
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

    def __repr__(self):  # you don't need to understand the implementation of this method
        def printree(root):
            if not root:
                return ["#"]

            root_key = str(root.key)
            left, right = printree(root.left), printree(root.right)

            lwid = len(left[-1])
            rwid = len(right[-1])
            rootwid = len(root_key)

            result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]

            ls = len(left[0].rstrip())
            rs = len(right[0]) - len(right[0].lstrip())
            result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

            for i in range(max(len(left), len(right))):
                row = ""
                if i < len(left):
                    row += left[i]
                else:
                    row += lwid * " "

                row += (rootwid + 2) * " "

                if i < len(right):
                    row += right[i]
                else:
                    row += rwid * " "

                result.append(row)

            return result

        return '\n'.join(printree(self.root))


if __name__ == "__main__":
    tree = AVLTree()

    # הכנסה של צמתים לעץ
    tree.insert(10, 'A')
    tree.insert(20, 'B')
    tree.insert(5, 'C')
    tree.insert(15, 'D')
    tree.insert(21, 'E')
    tree.insert(40, 'F')

    # בסוף כל ההכנסות, נדפיס את מבנה העץ לאחר האיזונים
    print("\nFinal tree structure:")
    print(tree)

