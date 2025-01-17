/**
 * FibonacciHeap
 *
 * An implementation of Fibonacci heap over positive integers.
 */
public class FibonacciHeap {

	/**
	 * Constructor to initialize an empty heap.
	 */
	public FibonacciHeap() {
	}

	/**
	 * pre: key > 0
	 * Insert (key, info) into the heap and return the newly generated HeapNode.
	 */
	// Complexity: O(1)
	public HeapNode insert(int key, String info) {
		meld(heap2);
	}

	/**
	 * Return the minimal HeapNode, null if empty.
	 */
	// Complexity: O(1)
	public HeapNode findMin() {
	}

	// Complexity: O(1)
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
		currCons.parent = null;
		HeapNode[] consArr = new HeapNode[maxTrees];
		HeapNode nextCons = null;
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
	}

	// Complexity: O(1)
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
			meld(newHeap);
		}
	}

	/**
	 * Delete the x from the heap.
	 */
	public void delete(HeapNode x) {
		return;
	}

	/**
	 * Return the total number of links.
	 */
	public int totalLinks() {
		return 0;
	}

	/**
	 * Return the total number of cuts.
	 */
	public int totalCuts() {
		return 0;
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
	}

	/**
	 * Return the number of trees in the heap.
	 */
	// Complexity: O(1)
	public int numTrees() {
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
