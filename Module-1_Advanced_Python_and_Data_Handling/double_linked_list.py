class Node:
    """A single node in a linked list."""

    def __init__(self, value):
        self.value = value   # The data this node holds
        self.next = None     # Reference to the next node (None if this is the last)
        self.prev = None     # Reference to the previous node (None if this is the first)

    def __repr__(self):
        return f"Node({self.value})"
    
class DoubleLinkedList:
    """A double linked list."""

    def __init__(self):
        self.head = None  # The list starts empty
        self.tail = None # Keep track of the tail for O(1) insertions at the end

    def insert_at_beginning(self, value):
        """Add a new node at the front of the list. O(1) time."""
        new_node = Node(value)
        new_node.next = self.head  # New node points to the old head
        if self.head is not None: 
            self.head.prev = new_node  # Old head's prev points to the new node
        self.head = new_node       # New node becomes the new head
        

    def insert_at_end(self, value):
        """Add a new node at the end of the list. O(n) time — must traverse to the end."""
        new_node = Node(value)
        if self.tail is None:      # List is empty
            self.head = new_node
            self.tail = new_node
            return
        new_node.prev = self.tail  # New node's prev points to the current tail
        self.tail.next = new_node  # Current tail's next points to the new node
        self.tail = new_node       # New node becomes the new tail

    def search(self, target):
        """Find a value in the list. Returns True/False. O(n) time."""
        current = self.head
        while current:
            if current.value == target:
                return True
            current = current.next  # Follow the pointer to the next node
        return False

    def display(self):
        """Print the list in a readable format."""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.value))
            current = current.next
        print(" -> ".join(elements) + " -> None")
    
    def display_reverse(self):  
        """Print the list in reverse order."""
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.value))
            current = current.prev  # Follow the pointer to the previous node
        print(" -> ".join(elements) + " -> None")
    
    def delete(self, target):
        """Remove the first node with the given value. Return True if found, False if not."""
        # Your code here
        if self.head is None:  # Empty list
            return False
        if self.head.value == target:  # Target is at the head
            self.head = self.head.next  # Move head to the next node
            return True
        current = self.head
        while current.next:
            if current.value == target:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                else:  # If we're deleting the tail, update the tail reference
                    self.tail = current.prev
                return True
            current = current.next
        return False


    def length(self):
        """Return the number of nodes in the list. O(n) time."""
        # Your code here
        count = 0 
        current = self.head
        while current:
            count += 1
            current = current.next
        return count


    def to_list(self):
        """Convert the linked list to a Python list. Returns a list of values."""
        # Your code here
        elements = []
        current = self.head
        while current:
            elements.append(current.value)
            current = current.next
        return elements


