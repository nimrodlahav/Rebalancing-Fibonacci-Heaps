/**
 * FibonacciHeap
 *
 * An implementation of Fibonacci heap over positive integers.
 */
public class FibonacciHeap {
	public HeapNode minimum;
	public int size;
	public int numberOfTrees;
	public int cuts = 0;
	public int links = 0;

	/**
	 * Constructor to initialize an empty heap.
	 */
	public FibonacciHeap() {
		minimum = null;
		size = 0;
		numberOfTrees = 0;
	}

	// Constructor to initialize an one-node heap
	public FibonacciHeap(int key, String info) {
		minimum = new HeapNode(key, info);
		size = 1;
		numberOfTrees = 1;
	}

	/**
	 * pre: key > 0
	 * Insert (key, info) into the heap and return the newly generated HeapNode.
	 */
	// Complexity: O(1)
	public HeapNode insert(int key, String info) {
		FibonacciHeap heap2 = new FibonacciHeap(key, info);
		HeapNode insertedNode = heap2.minimum;
		meld(heap2);
		return insertedNode;
	}

	/**
	 *
	 * Return the minimal HeapNode, null if empty.
	 *
	 */
	// Complexity: O(1)
	public HeapNode findMin() {return minimum;}

	// Complexity: O(1)
	public HeapNode link(HeapNode x, HeapNode y)
	{
		links++; // Count current link
		if (x.key > y.key) {
			HeapNode tmp = x;
			x = y;
			y = tmp;
		}
		y.parent = x;
		if (x.child == null)
			x.child = y.prev = y.next = y;
		else { // X's rank > 0
			y.next = x.child;
			y.prev = x.child.prev;
			x.child.prev.next = y;
			x.child.prev = y;
		}
		return x;
	}

	/**
	 *
	 * Delete the minimal item
	 *
	 */
	// Complexity: W.C O(n), Amortize O(logn)
	public void deleteMin()
	{
		// Empty or one node heap cases
		if (minimum == null || size == 1) {
			size = numberOfTrees = 0;
			minimum = null;
			return;
		}

		HeapNode currCons = null;
		if (minimum.child != null) { // Start consolidating from minimum's child
			currCons = minimum.child;
			// Connect deleted node children to roots list
			minimum.child.prev.next = minimum.next;
			minimum.next.prev = minimum.child.prev;
			currCons.parent = null;
		} else // Start consolidating from minimum's next
			currCons = minimum.next;
		currCons.prev = minimum.prev;
		minimum.prev.next = currCons;
		// Disconnect minimum from heap
		minimum.prev = minimum.next = minimum.child = minimum;
		size--;

		int maxTrees = (int) Math.ceil(Math.log(size) / Math.log(2)) + 1; // Max number of trees in a valid Fibonacci Heap
		HeapNode[] consArr = new HeapNode[maxTrees];
		HeapNode firstCons = currCons;
		HeapNode nextCons = null; // Save next tree to consolidate

		do {
			// Temporary disconnect tree to consolidate from the heap
			currCons.prev = currCons;
			nextCons = currCons.next;
			currCons.next = currCons;
			int currRank = currCons.rank;

			for (int i = currRank; i < maxTrees; i++) {
				if (consArr[currRank] == null) { // Current bucket is empty
					consArr[currRank] = currCons;
					break;
				}
				// Perform link operation with both trees in the bucket
				else if (i < maxTrees - 1) { // Link operation cannot be performed in last bucket
					HeapNode root = link(currCons, consArr[currRank]);
					// Move linked tree to the next bucket
					consArr[currRank] = null;
					consArr[currRank + 1] = root;
					root.rank++;
				}
			}
			currCons = nextCons; // Continue consolidating with next tree
		} while (currCons != firstCons);

		minimum = null;
		for (HeapNode root : consArr) {
			if (root != null) {
				numberOfTrees++;
				if (minimum == null)
					minimum = root;
				connectRoots(root, minimum);
			}
		}
	}

	// Complexity: O(1)
	public void connectRoots(HeapNode x, HeapNode y) {
		x.next.prev = y.prev;
		y.prev.next = x.next;
		x.next = y;
		y.prev = x;
		// Update heap's fields
		if (x.key > y.key)
			minimum = y;
		else
			minimum = x;
	}

	// Complexity: O(1)
	public void cut(HeapNode x, HeapNode y)
	{
		cuts++; // Count current cut
		x.parent = null;
		x.mark = false;
		y.rank--;
		if (x.next == x)
			y.child = null;
		else { // X isn't y's only child
			y.child = x.next;
			x.next.parent = y;
			x.prev.next = x.next;
			x.next.prev = x.prev;
		}
		// Disconnect x from its current position
		x.parent = null;
		x.prev = x.next = x;
		connectRoots(x, minimum); // Add x to heap as a root
		numberOfTrees++; // Update heap's trees number
	}

	// Complexity: W.C O(logn), Amortize O(1)
	public void cascadingCut(HeapNode x, HeapNode y)
	{
		cut(x,y);
		if (y.parent != null) {
			if (y.mark == false) // Non-root node lost its first child, and therefore becomes marked
				y.mark = true;
			else { // Non-root node lost its second child, and therefore is being cut
				cascadingCut(y,y.parent);
			}
		}
	}

	/**
	 *
	 * pre: 0<diff<x.key
	 *
	 * Decrease the key of x by diff and fix the heap.
	 *
	 */
	// Complexity: W.C O(logn), Amortize O(1)
	public void decreaseKey(HeapNode x, int diff)
	{
		if (x == null) return; // Edge case
		x.key -= diff;
		if (x.parent != null && x.key < x.parent.key) { // Heap property violation
			HeapNode y = x.parent;
			cascadingCut(x,y);
		}
	}

	/**
	 *
	 * Delete the x from the heap.
	 *
	 */
	// Complexity: W.C O(logn), Amortize O(1)
	public void delete(HeapNode x)
	{
		if (x != minimum) {
			decreaseKey(x, x.key-1); // Now x is the minimum
			// Disconnect deleted node from the heap
			x.prev.next = x.next;
			x.next.prev = x.prev;
			x.prev = x.next = x;
			size--; // Update heap's size
		}
		else // Deleted node is heap's minimum
			deleteMin();
	}

	/**
	 *
	 * Return the total number of links.
	 *
	 */
	// Complexity: O(1)
	public int totalLinks() {return links;}

	/**
	 *
	 * Return the total number of cuts.
	 *
	 */
	// Complexity: O(1)
	public int totalCuts() {return cuts;}

	/**
	 *
	 * Meld the heap with heap2
	 *
	 */
	// Complexity: O(1)
	public void meld(FibonacciHeap heap2)
	{
		if (heap2 == null) return; // Edge case
		HeapNode min2 = heap2.minimum;
		if (minimum != null && min2 != null) {
			connectRoots(minimum, min2); // Connect both heaps with minimum nodes
		}
		else if (minimum == null) // Heap is empty
			minimum = min2;
		numberOfTrees += heap2.numberOfTrees;
		size += heap2.size;
	}

	/**
	 *
	 * Return the number of elements in the heap
	 *
	 */
	// Complexity: O(1)
	public int size() {return size;}

	/**
	 *
	 * Return the number of trees in the heap.
	 *
	 */
	// Complexity: O(1)
	public int numTrees() {return numberOfTrees;}

	/**
	 * Class implementing a node in a Fibonacci Heap.
	 *
	 */




	public int potential() {
		int t = 0; // Number of trees (roots)
		int m = 0; // Number of marked nodes
		HeapNode current = minimum;

		if (current != null) {
			// Traverse the circular linked list of roots
			do {
				t++; // Each root is a tree
				m += countMarkedNodes(current); // Count marked nodes in the tree
				current = current.next;
			} while (current != minimum);
		}

		return t + 2 * m; // Potential is t + 2 * m
	}

	// Helper method to count marked nodes in a tree
	private int countMarkedNodes(HeapNode node) {
		int count = 0;
		while (node != null) {
			if (node.mark) count++; // Increment if the node is marked
			node = node.child;
		}
		return count;
	}

	public int[] countersRep() {
		int[] counters = new int[calculateMaxRank()]; // Array to store the number of trees of each rank
		HeapNode current = minimum;

		// Traverse the root list and count trees by rank
		if (current != null) {
			do {
				int rank = current.rank;
				counters[rank]++; // Increment the count of trees of this rank
				current = current.next;
			} while (current != minimum);
		}

		return counters;
	}

	// Helper method to calculate the maximum possible rank (based on the number of nodes in the heap)
	private int calculateMaxRank() {
		return (int) Math.ceil(Math.log(size) / Math.log(2)) + 1;
	}

	public boolean empty() {
		if (size == 0)
			return true;
		return false;
	}






	public static class HeapNode{
		public int key;
		public String info;
		public HeapNode child;
		public HeapNode next;
		public HeapNode prev;
		public HeapNode parent;
		public int rank;
		public boolean mark;

		// Constructor to initialize a HeapNode
		public HeapNode(int key, String info) {
			this.key = key;
			this.info = info;
			next = this;
			prev = this;
		}



		public int getKey() {
			return key;
		}

	}