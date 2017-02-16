
import unittest


# An implementation of a d-ary heap (aka d-way heap or d-heap) with an implicit array-based structure, using a python
# list as an array.
#
# A d-ary heap is a binary heap, but with an arbitrary branching factor.
class DHeap:

    @staticmethod
    def heapify(unordered_list, max_heap=True, branching_factor=2):
        """
        Takes an existing list and turns it into a heap.
        Completes in O(n log n) time.
        :param unordered_list: The array to heapify.
        :param max_heap: True to create a max heap, else False to create a min heap.
        :param branching_factor: The maximum number of children each parent in the tree should have. Defaults to 2 for
        a binary tree.
        :return: A heap wrapping the given list, after it has heapified the list.
        """
        heap = DHeap(max_heap=max_heap, branching_factor=branching_factor)
        heap.heap_array = unordered_list
        heap.last_index = len(unordered_list) - 1

        # Starts at the parent of the heap's last node.
        start = (heap.last_index - 1) // heap.branching_factor

        # Sifts down each parent in the tree until all parents in the tree have been made to satisfy the heap property.
        while start >= 0:
            heap.__sift_down(start)
            start -= 1

        return heap

    @staticmethod
    def heapsort(unordered_list, ascending=True):
        """
        Uses binary heap logic in order to sort a given list in place. Takes an average of O(n log n) time.
        :param unordered_list: The list to order in place.
        :param ascending: True to sort into ascending order, else False to order in descending order.
        """
        # Step 1: turns the list into a heap.
        heap = DHeap.heapify(unordered_list, max_heap=ascending)

        # Step 2: Pops each element off the heap, but keeps them in the list, ordered, rather than removing them.
        while heap.last_index >= 0:
            # swaps the first and last elements of the heap.
            heap.__swap(0, heap.last_index)
            heap.last_index -= 1

            # recursively heapifies the new top element downwards until its in its correct position.
            heap.__sift_down(0)

    def __init__(self, initial_contents=(), max_heap=True, branching_factor=2):
        """
        Class constructor. Completes in O(n log n) time.
        :param initial_contents: The contents to initially store in the heap. Copies the given values and does not edit
        the passed in list.
        :param max_heap: True to create a max heap, else False to create a min heap.
        :param branching_factor: The maximum number of children each parent in the tree should have. Defaults to 2 for

        """
        self.branching_factor = branching_factor
        self.max_heap = max_heap
        self.heap_array = []
        self.last_index = -1

        # Pushes each initializing value into the heap.
        for val in initial_contents:
            self.push(val)

    def peek(self):
        """
        Gets the root of the heap without removing it, if it exists.
        Completes in O(1) time.
        :return: The heap's root value.
        """
        return self.heap_array[0]

    def pop(self):
        """
        Removes and gets the root of the heap, if it exists.
        Completes in O(log n) time.
        :return: The heap's root value.
        """

        # makes note of the value to return
        ret_val = self.peek()

        # swaps the first and last elements of the heap, then removes the new last element (the one being popped)
        self.__swap(0, self.last_index)
        self.heap_array.pop(self.last_index)
        self.last_index -= 1

        # recursively heapifies the new top element downwards until its in its correct position
        self.__sift_down(0)

        return ret_val

    def push(self, val):
        """
        Adds a value to the heap.
        Completes in O(log n) time.
        :@param val: The value to push onto the heap.
        """
        # initially adds the value to the end of the array
        self.last_index += 1
        self.heap_array.append(val)

        # recursively sifts the value up until it finds a valid position in the heap
        self.__sift_up(self.last_index)

    def __swap(self, index_1, index_2):
        """
        Swaps the contents of two slots of the heap.
        :param index_1: The first index.
        :param index_2: The second index.
        """
        self.heap_array[index_1], self.heap_array[index_2] = self.heap_array[index_2], self.heap_array[index_1]

    def __compare(self, index_1, index_2):
        """
        Compares two values depending on whether this is a max or min heap.
        :param index_1: The index of the first value.
        :param index_2: The index of the second value.
        :return: True if the first value should be higher up in the heap than the second value, else False.
        """
        if self.max_heap:
            return self.heap_array[index_1] > self.heap_array[index_2]
        else:
            return self.heap_array[index_1] < self.heap_array[index_2]

    def __sift_up(self, index):
        """
        Takes the index of an element that may violate the heap requirements and recursively swaps it with its ancestors
        until it finds a valid place.
        :param index: The index to start at.
        """
        parent = (index - 1) // self.branching_factor
        if parent >= 0 and self.__compare(index, parent):
            self.__swap(index, parent)
            self.__sift_up(parent)

    def __sift_down(self, index):
        """
        Takes the index of an element that may violate the heap requirements and recursively swaps it with its children
        until it finds a valid place.
        :param index: The index to start with.
        """
        new_parent = index  # largest defaults to parent, then tested against the children's values

        # finds the largest node among the parent and its children
        i = 1
        while i <= self.branching_factor:

            child = (index * self.branching_factor) + i

            # if the child exists and is better than the parent and any other children checked so far, marked as the
            # new parent
            if child <= self.last_index and self.__compare(child, new_parent):
                new_parent = child

            i += 1

        # if the new parent differs from the old parent, swap the two and continue recursively heapifying
        if new_parent is not index:
            self.__swap(index, new_parent)
            self.__sift_down(new_parent)

    def validate_heap(self, parent=0):
        """
        Recursively validates that this satisfies the heap requirements.
        :param parent: The index of the parent to start with. Checks the tree below this index. 0 to check the entire
         heap.
        :return: True if the tree including this parent and all its children is valid, Else False.
        """
        first_child = (parent * self.branching_factor) + 1

        # Checks each child against its parent, and recursively checks any further descendants against their parents.
        i = 0
        while i < self.branching_factor:
            child = first_child + i
            if child <= self.last_index:
                # Base case: parent and child are out of order.
                if self.__compare(child, parent):
                    return False
                # Recursive call to check the children of the child.
                else:
                    return self.validate_heap(child)
            i += 1

        # Base case: Reached a leaf without finding any inconsistencies.
        return True

    def __str__(self):
        return self.heap_array.__str__()

    def __repr__(self):
        return self.heap_array.__repr__()

    def __len__(self):
        return self.last_index + 1


# Unit tests for DHeap
class DHeapTest(unittest.TestCase):

    def test_binary_heap_construction(self):
        """Tests creating a binary heap from an existing list without modifying the passed in list."""
        source = [1, 1, 5, 10, -23, 105]
        heap = DHeap(source)
        self.assertEqual(heap.validate_heap(), True)
        self.assertListEqual(source, [1, 1, 5, 10, -23, 105])

    def test_ternary_heap_construction(self):
        """Tests creating a ternary heap from an existing list without modifying the passed in list."""
        source = [1, 1, 5, 10, -23, 105, 1200412, -2352, 0, 0, 101, 45, -2]
        heap = DHeap(source, branching_factor=3)
        self.assertEqual(heap.validate_heap(), True)
        self.assertListEqual(source, [1, 1, 5, 10, -23, 105, 1200412, -2352, 0, 0, 101, 45, -2])

    def test_heapify(self):
        """Tests turning an existing list into a heap."""
        source = [1, 0, 5, 103, -23, -2213415]
        heap = DHeap.heapify(source)
        self.assertEqual(heap.validate_heap(), True)

    def test_heapsort(self):
        """Tests the heapsort implementation using a DHeap."""
        unordered = [1, 5, 64, 64, 12315, 677, -15, -1002]
        DHeap.heapsort(unordered, True)
        self.assertListEqual(unordered, [-1002, -15, 1, 5, 64, 64, 677, 12315])

    def test_push(self):
        """Tests pushing values onto a heap."""
        heap = DHeap()
        heap.push(1)
        self.assertEqual(heap.validate_heap(), True)
        heap.push(0)
        self.assertEqual(heap.validate_heap(), True)
        heap.push(-1)
        heap.push(10)
        heap.push(100)
        heap.push(-1)
        heap.push(-5)
        self.assertEqual(heap.validate_heap(), True)

    def test_peek(self):
        """Tests peeking the top value from the heap."""
        heap = DHeap([1, 1, 5, 10, -23, 105])
        self.assertEqual(heap.validate_heap(), True)
        self.assertEqual(heap.peek(), 105)
        heap.push(1000)
        self.assertEqual(heap.peek(), 1000)

    def test_pop(self):
        """Tests popping values off of the heap."""
        heap = DHeap([-10, 0, 5, -2, 5, 1024, -999])
        self.assertEqual(heap.validate_heap(), True)
        self.assertEqual(heap.pop(), 1024)
        self.assertEqual(heap.validate_heap(), True)
        self.assertEqual(heap.pop(), 5)
        self.assertEqual(heap.pop(), 5)
        self.assertEqual(heap.pop(), 0)
        self.assertEqual(heap.pop(), -2)
        self.assertEqual(heap.pop(), -10)
        self.assertEqual(heap.pop(), -999)
        self.assertEqual(heap.validate_heap(), True)

    def test_min_heap(self):
        """Tests using a min heap rather than the default max heap."""
        heap = DHeap([-10, 0, 5, -2, 5, 1024, -999])
        self.assertEqual(heap.validate_heap(), True)
        heap.push(12)
        self.assertEqual(heap.validate_heap(), True)
        self.assertEqual(heap.pop(), 1024)
