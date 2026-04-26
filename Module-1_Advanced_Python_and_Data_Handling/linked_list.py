class Node:
    """A single node in a linked list."""

    def __init__(self, value):
        self.value = value   # The data this node holds
        self.next = None     # Reference to the next node (None if this is the last)

    def __repr__(self):
        return f"Node({self.value})"
    
class LinkedList:
    """A singly linked list."""

    def __init__(self):
        self.head = None  # The list starts empty

    def insert_at_beginning(self, value):
        """Add a new node at the front of the list. O(1) time."""
        new_node = Node(value)
        new_node.next = self.head  # New node points to the old head
        self.head = new_node       # New node becomes the new head

    def insert_at_end(self, value):
        """Add a new node at the end of the list. O(n) time — must traverse to the end."""
        new_node = Node(value)
        if self.head is None:      # List is empty
            self.head = new_node
            return
        current = self.head
        while current.next:        # Walk to the last node
            current = current.next
        current.next = new_node    # Last node now points to the new node

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
            if current.next.value == target:
                current.next = current.next.next  # Bypass the node to be deleted
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


#Test Methods

ll = LinkedList()
for val in [10, 20, 30, 40, 50]:
    ll.insert_at_end(val)

ll.display()           # 10 -> 20 -> 30 -> 40 -> 50 -> None
print(ll.length())     # 5
ll.delete(30)
ll.display()           # 10 -> 20 -> 40 -> 50 -> None
print(ll.to_list())    # [10, 20, 40, 50]

#Write a function that checks whether a string of brackets is properly balanced using a stack:

def is_balanced(text):
    """Return True if all brackets in text are properly matched.
    Handles: (), [], {}
    """
    # Your code here
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in text:
        if char in pairs.values():  # If it's an opening bracket
            stack.append(char)
        elif char in pairs:         # If it's a closing bracket
            if not stack or stack[-1] != pairs[char]:  # Check for mismatch or empty stack
                return False
            stack.pop()  # Pop the matching opening bracket
    return len(stack) == 0  # True if no unmatched opening brackets remain

# Tests:
print(is_balanced("()"))           # True
print(is_balanced("({[]})"))       # True
print(is_balanced("(]"))           # False
print(is_balanced("([)]"))         # False
print(is_balanced("hello (world)")) # True