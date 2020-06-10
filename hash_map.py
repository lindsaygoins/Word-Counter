# Author: Lindsay Goins
# Description: Implementation of a Hash Map using a list and linked list. This hash map handles collisions
# via chaining.


class SLNode:
    """Represents a node in a linked list."""

    def __init__(self, key, value):
        """Initializes a Node object."""
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        """Prints the node and its value in a readable format."""
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    """Represents a linked list."""

    def __init__(self):
        """Initializes a Linked List with a head and a size of 0."""
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """
        Summary: Creates a new node and inserts it at the front of the linked list.
        Parameters: Key (the key for the node), Value (the value for the node)
        """
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """
        Summary: Removes a node from the linked list.
        Parameters: Key (the key of the node to remove)
        Returns: True if the node is removed, otherwise False.
        """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """
        Summary: Searches the linked list for a node with a given key
        Parameters: Key (key of the node)
        Returns: Returns the node that matches the key, otherwise None.
        """
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        """Prints out a readable form of the linked list."""
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """Represents a hash map that holds key-value pairs. Handles collisions by chaining."""

    def __init__(self, capacity, function):
        """
        Summary: Initializes a Hash Map via a list and linked list structure. It is initialized with the specified
        number of buckets and a specified hash function.
        Parameters: Capacity (number of buckets to be created) and Function (specific function used to hash keys)
        """
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Summary: Deletes all elements in the hash table.
        """
        for bucket in self._buckets:
            bucket.head = None
            bucket.size = 0
        self.size = 0

    def get(self, key):
        """
        Summary: Returns the value with the given key.
        Parameters: Key
        Returns: The value that is associated with the key, otherwise it returns None if there is no such value.
        """
        index = self._hash_function(key) % self.capacity
        if self._buckets[index].contains(key):
            return self._buckets[index].contains(key).value
        else:
            return None

    def resize_table(self, capacity):
        """
        Summary: Resizes the hash table to have a number of buckets equal to the specified capacity.
        Parameters: Capacity (the new number of buckets)
        """
        new_map = HashMap(capacity, self._hash_function)
        count_bucket = 0
        for bucket in self._buckets:
            count_bucket += 1
            if bucket.head is not None:
                cur_node = self._buckets[count_bucket - 1].head

                # Rehashes the keys in the new hash map
                while cur_node is not None:
                    new_index = self._hash_function(cur_node.key) % capacity
                    new_node = SLNode(cur_node.key, cur_node.value)

                    # Adds new nodes to the new hash map
                    if new_map._buckets[new_index].head is None:
                        new_map._buckets[new_index].head = new_node
                        pointer = new_node
                    else:
                        pointer.next = new_node
                        pointer = pointer.next
                    cur_node = cur_node.next

        # Changes the pointers to point to the new hash map
        self._buckets = new_map._buckets
        self.capacity = capacity

    def put(self, key, value):
        """
        Summary: Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.
        Parameters: Key and Value
        """
        index = self._hash_function(key) % self.capacity
        if self._buckets[index].contains(key):
            self._buckets[index].contains(key).value = value
        else:
            self._buckets[index].add_front(key, value)
            self.size += 1

    def remove(self, key):
        """
        Summary: Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing.
        Parameters: Key
        """
        index = self._hash_function(key) % self.capacity
        cur_node = self._buckets[index].head
        if self._buckets[index].contains(key):
            while cur_node is not None:
                self._buckets[index].remove(key)
                cur_node = cur_node.next
            self.size -= 1

    def contains_key(self, key):
        """
        Summary: Searches to see if a key exists within the hash table.
        Returns: True if the key is found, and False otherwise.
        """
        index = self._hash_function(key) % self.capacity
        if self._buckets[index].contains(key):
            return True
        else:
            return False

    def empty_buckets(self):
        """
        Summary: Counts the number of empty buckets in the table.
        Returns: The number of empty buckets in the table.
        """
        count_empty = 0
        for bucket in self._buckets:
            if bucket.head is None:
                count_empty += 1
        return count_empty

    def table_load(self):
        """
        Summary: Calculates the load factor, which is the ratio between the number of links and the number of buckets
        in the table.
        Returns: The load factor (as a float).
        """
        count_link = 0
        for bucket in self._buckets:
            cur_node = bucket.head
            while cur_node is not None:
                count_link += 1
                cur_node = cur_node.next

        return count_link / self.capacity

    def __str__(self):
        """
        Summary: Prints all the links in each of the buckets in the table.
        """
        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

