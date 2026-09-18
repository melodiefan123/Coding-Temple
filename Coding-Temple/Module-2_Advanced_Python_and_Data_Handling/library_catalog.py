class Book: 
    def __init__(self, title, author, year, pages):
        self.title = title
        self.author = author
        if year > 0: 
            self.year = year
        else:
            raise ValueError("Year must be a positive integer.")
        self.checked_out = False
        if pages > 0: 
            self.pages = pages
        else:
            raise ValueError("Number of pages must be a positive integer.")

      
    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False

    def __lt__(self, other):
         if isinstance(other, Book):
            return (self.title) < (other.title)
         return NotImplemented

    def __len__(self):
        return self.pages
      
    def __contains__(self, keyword):
        return keyword.lower() in self.title.lower() or keyword.lower() in self.author.lower()
    
    def check_out(self):
        if self.checked_out:
            print(f"Sorry, '{self.title}' is already checked out.")
        else:
            self.checked_out = True
            print(f"You have checked out '{self.title}'. Enjoy reading!")
    
    def return_book(self):
        if self.checked_out:
            self.checked_out = False
            print(f"Thank you for returning '{self.title}'.")
        else:
            print(f"'{self.title}' was not checked out and still available.")
    
    def __repr__(self):
        status = "Checked Out" if self.checked_out else "Available"
        return f"'{self.title}' by {self.author} ({self.year}) - {status}"


class EBook(Book):
    def __init__(self, title, author, year, pages,file_size_mb):
        super().__init__(title, author, year, pages)
        if file_size_mb > 0: 
            self.file_size_mb = file_size_mb
        else:
            raise ValueError("File size must be a positive number.")
        self.checkout_count = 0 
    
    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr} [E-Book, {self.file_size_mb} MB]"
    
    
    def check_out(self):
        self.checkout_count += 1
        return f"{self.title} has been checked out {self.checkout_count} times."
    
class Catalog:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        if isinstance(book, Book):
            self.books.append(book)
            print(f"Added '{book.title}' to the catalog.")
        else:
            print("Only Book instances can be added to the catalog.")
    
    def search_by_author(self, author):
        found_books = [book for book in self.books if book.author == author]
        if not found_books:
            print(f"No books found by {author}.")
        else:
            for book in found_books:
                print(book)
    
    def search_by_title(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        if not found_books:
            return f"No books found with the title '{title}'."
        else:
            return found_books

                
    
    def get_available(self):
        available_books = [book for book in self.books if not book.checked_out or isinstance(book, EBook)]
        return available_books
    
    def summary(self):
        total_books = len(self.books)
        checked_out_books = sum(1 for book in self.books if book.checked_out)
        available_books = total_books - checked_out_books
        print(f"Catalog Summary: Total Books: {total_books}, Available: {available_books}, Checked Out: {checked_out_books}")


#Test Cases

catalog = Catalog()
catalog.add_book(Book("Python Crash Course", "Eric Matthes", 2019, 500))
catalog.add_book(Book("Clean Code", "Robert Martin", 2008, 450))
catalog.add_book(EBook("AI Engineering", "Chip Huyen", 2025, 15.2,300))

#Sorted Books
sorted_books = sorted(catalog.books)
print(f"Books sorted by title: {sorted_books}")

# Search
results = catalog.search_by_title("python")
print(results)  # Should find "Python Crash Course"

# Check out
catalog.books[0].check_out()
available = catalog.get_available()
print(f"Available: {len(available)} books")

catalog.summary()
