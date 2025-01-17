/**
 * FibonacciHeap
 *
 * An implementation of Fibonacci heap over positive integers.
 */
public class FibonacciHeap {
	public HeapNode minimum;
	public int size;
	public int numberOfTrees = 0;
	public int cuts = 0;			// new field for totalCuts
	public int links = 0;			// " " " totalLinks

	/**
	 * Constructor to initialize an empty heap.
	 */
	public FibonacciHeap() {
		minimum = null;
		size = 0;
		numberOfTrees = 0;
	}

	public FibonacciHeap(int key, String info) {			// constructor of on-node heap
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
		HeapNode newRoot = new HeapNode();
		newRoot.key = key;
		newRoot.info = info;
		FibonacciHeap heap2 = new FibonacciHeap();			// why create a new one (and not use "this")?
		heap2.minimum = newRoot;
		heap2.size = heap2.numberOfTrees = 1;
		meld(heap2);
		return newRoot;
	}

	/**
	 * Return the minimal HeapNode, null if empty.
	 */
	// Complexity: O(1)
	public HeapNode findMin() {
		return minimum;
	}

	// Complexity: O(1)
	public HeapNode link(HeapNode x, HeapNode y) {				// where should i put a link counter?
		if (x.key > y.key) {
			HeapNode tmp = x;
			x = y;
			y = tmp;
		}
		if (x.child == null)
			y.next = y;
		else {
			y.next = x.child.next;
			x.child.next = y;
		}
		return x;
	}

	/**
	 * Delete the minimal item
	 */
	// Complexity: W.C O(n), Amortize O(logn)
	public void deleteMin() {
		HeapNode currCons = minimum.child;			// what's the meaning of the variable name?
		currCons.parent = null;
		currCons.next = minimum.next;
		minimum.prev.next = minimum.next.prev = currCons;
		minimum.prev = minimum.next = null;
		int maxTrees = (int) Math.log(size + 1);
		HeapNode[] consArr = new HeapNode[maxTrees];
		HeapNode nextCons = null;
		while (nextCons != minimum.child) {
			currCons.prev = null;
			nextCons = currCons.next;
			currCons.next = null;
			int currRank = currCons.rank;
			for (int i = currRank; i < maxTrees - 1; i++) {
				if (consArr[currRank] == null) {
					consArr[currRank] = currCons;
					break;
				} else {
					HeapNode root = link(currCons, consArr[currRank]);
					this.links += 1;
					consArr[currRank] = null;
					consArr[currRank + 1] = root;
				}
				currCons = nextCons;
			}
		}
		HeapNode[] contiguousArr = new HeapNode[maxTrees];
		int rankCnt = 0;
		HeapNode newMin = null;
		int newMinKey = Integer.MAX_VALUE;
		for (int i = 0; i < consArr.length; i++) {
			if (consArr[i] != null) {
				contiguousArr[rankCnt] = consArr[i];
				rankCnt++;
				if (consArr[i].key < newMinKey) {
					newMin = consArr[i];
					newMinKey = consArr[i].key;
				}
			}
		}
		for (int i = 0; i < rankCnt; i++) {
			if (i != rankCnt) {
				contiguousArr[i].next = contiguousArr[i + 1];
				if (i > 0)
					contiguousArr[i].prev = contiguousArr[i - 1];
				else
					contiguousArr[i].prev = contiguousArr[rankCnt];
			} else {
				contiguousArr[i].prev = contiguousArr[Math.max(rankCnt - 1, 0)];
				contiguousArr[i].next = contiguousArr[0];
			}
		}
		minimum = newMin;
		size--;
		numberOfTrees = rankCnt;
	}

	// Complexity: O(1)
	public void cut(HeapNode x, HeapNode y) {			// where do i keep the cut counter?
		x.parent = null;
		x.mark = false;
		y.rank--;
		if (x.next == x)
			y.child = null;
		else {
			y.child = x.next;
			x.prev.next = x.next;
			x.next.prev = x.prev;
		}
	}

	// Complexity: O(1)
	public void cascadingCut(HeapNode x, HeapNode y) {
		cut(x, y);
		this.cuts += 1;
		if (y.parent != null) {
			if (!y.mark)
				y.mark = true;
			else
				cascadingCut(y, y.parent);
		}
	}

	/**
	 * pre: 0 < diff < x.key
	 * Decrease the key of x by diff and fix the heap.
	 */
	// Complexity: W.C O(logn), Amortize O(1)
	public void decreaseKey(HeapNode x, int diff) {
		x.key -= diff;
		if (x.key < x.parent.key) {
			HeapNode y = x.parent;
			cascadingCut(x, y);
			FibonacciHeap newHeap = new FibonacciHeap();
			newHeap.minimum = x;
			meld(newHeap);
		}
	}

	/**
	 * Delete the x from the heap.
	 */
	public void delete(HeapNode x) {
		this.decreaseKey(x, (x.key)-(x.minimum+1));		// now x is the minimum
		this.deleteMin();
		return;
	}

	/**
	 * Return the total number of links.
	 */
	public int totalLinks() {
		return links;
	}

	/**
	 * Return the total number of cuts.
	 */
	public int totalCuts() {
		return cuts;
	}

	/**
	 * Meld the heap with heap2
	 */
	public void meld(FibonacciHeap heap2) {
		return;
	}

	/**
	 * Return the number of elements in the heap
	 */
	// Complexity: O(1)
	public int size() {
		return size;
	}

	/**
	 * Return the number of trees in the heap.
	 */
	// Complexity: O(1)
	public int numTrees() {
		return numberOfTrees;
	}

	/**
	 * Class implementing a node in a Fibonacci Heap.
	 */
	public static class HeapNode {
		public int key;
		public String info;
		public HeapNode child;
		public HeapNode next;
		public HeapNode prev;
		public HeapNode parent;
		public int rank;
		public boolean mark;
	}
}
