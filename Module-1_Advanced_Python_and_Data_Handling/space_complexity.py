# Function A: O(n) - Linear Space: Function creates a new data structure that grows with the input size. 
def reverse_string(s):
   return s[::-1]

# Function B: O(n) - Linear Space: Function creates a new data structure that grows with the input size. 
def count_letters(text):
   counts = {}
   for char in text:
       counts[char] = counts.get(char, 0) + 1
   return counts

# Function C: O(n^2) - Quadratic Space: Function creates a data structure that grows with the square of the input. 
def matrix_identity(n):
   return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

# Function D: O(1) Constant Space - No matter how many items the list contains, function only uses the total variable. 
def running_sum(numbers):
   total = 0
   for num in numbers:
       total += num
   print(total)

#Part 2 - Tradeoff Decision
# You have a function that processes a large CSV file (5 million rows). You need to find all duplicate email addresses. Write two approaches: one that loads all emails into a set (fast, more memory), and one that sorts the file and scans for adjacent duplicates (slower, less memory). In a comment above each, note the time and space complexity.

#Approach 1: Load all emails into a set (fast, more memory)
# Time: O(n) - single pass through all rows
# Space: O(n) - seen and duplicates sets grow with input size
def find_duplicates_set(csv):
   seen = set()
   duplicates = set()
   for row in csv: 
      email = row['email']
      if email in seen: 
         duplicates.add(email)
      else: 
         seen.add(email)
   return duplicates

#Approach 2: Sort the file and scan for adjacent duplicates (slower, less memory)
# Time: O(n log n) - sorting dominates
# Space: O(n) - stores sorted copy of all emails
def find_duplicates_sort(emails): 
   duplicates = set()
   sorted_emails = sorted(emails) 
   for i in range(1, len(sorted_emails)): 
      if sorted_emails[i] == sorted_emails[i-1]: 
         duplicates.add(sorted_emails[i])
   return duplicates
