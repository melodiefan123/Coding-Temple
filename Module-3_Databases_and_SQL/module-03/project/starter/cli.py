"""
Module 3 Project: Library Management System
cli.py — Command-line interface

Your job: Implement each menu handler function below.
The main menu loop is already provided — just fill in the handlers.
"""

from library_system import (
    init_db, add_author, add_book, add_member,
    checkout_book, return_book, find_books_by_author,
    get_overdue_books, get_popular_genres, get_available_books, engine, Session, Author
)


def menu_add_book():
    """Prompt for book details and add to the database."""
    # TODO: Use input() to collect title, isbn, author name, year, genres
    # Tip: You may need to add the author first if they don't exist
    # TODO: Call add_book() and print a confirmation message
    title = input("Please enter the title: ")
    isbn = int(input("Please enter the isbn:"))
    author_name = input("Please enter the author's name: ")
    try:
        author = add_author(name=author_name)
    except Exception:
        with Session(engine) as session:
            author = session.query(Author).filter_by(name=author_name).first()
    year = int(input("Enter the year the book was published:"))
    genres = input("Enter the book genre: ")
    books = add_book(title=title, isbn=isbn, author_id=author.id, published_year=year, genre_names = [genres])
    print(f"{books.title} has been added.")


def menu_add_borrower():
    """Prompt for borrower details and register in the database."""
    # TODO: Use input() to collect name, email, phone
    # TODO: Call add_borrower() and print a confirmation message
    name = input("Please enter your name:")
    email = input("Please enter your email address:")
    phone = input("Please enter your phone:")
    members = add_member(name=name, email=email, phone=phone)
    print(f"{members.name} has been added.")


def menu_checkout():
    """Prompt for book ID and borrower ID, then check out the book."""
    # TODO: Show available books (call get_available_books())
    # TODO: Prompt for book_id and borrower_id
    # TODO: Call checkout_book() and handle ValueError (book not available)
    available_books = get_available_books()
    for book in available_books: 
            print(f"{book.title} is available.")
    try: 
        book_id = int(input("Enter the book ID: "))
        member_id = int(input("Enter the member ID: "))
        results = checkout_book(book_id=book_id, member_id=member_id)  
        print(f"{results.books.title} has been checked out.")
    except ValueError: 
        print("Book not available")
    


def menu_return():
    """Prompt for checkout ID and return the book."""
    # TODO: Prompt for checkout_id, call return_book(), print confirmation
    checkout_id = int(input("Please enter the checkout ID:"))
    try:
        results = return_book(checkout_id=checkout_id)
        print(f"{results.books.title} has been returned.")
    except Exception:
        print("Please enter a valid checkout ID.")
        


def menu_search_by_author():
    """Prompt for author name and display matching books."""
    # TODO: Prompt for author_name, call find_books_by_author(), print results
    author_name = input("Please enter the author's name:")
    results = find_books_by_author(author_name=author_name)
    if not results: 
        print(f"No book found for that author.")
    else: 
        for result in results: 
            print(f"{result.title}")
            

def menu_overdue():
    """Display all overdue checkouts."""
    # TODO: Call get_overdue_books() and print results
    results = get_overdue_books()
    if not results: 
        print("No books are overdue.")
    else:
        for result in results: 
            print(f"Book_id: {result.book_id}\n Member_id:{result.member_id}\n Due_date:{result.due_date} ")

def menu_popular_genres():
    """Display the most popular genres by checkout count."""
    # TODO: Call get_popular_genres() and print results
    results = get_popular_genres()
    if not results: 
        print("No popular genres.")
    else:
        for result in results: 
            for book in result.book:
                print(f"Genre:{result.name} \nBook: {book.title}")

def main():
    init_db()

    while True:
        print("\n=== Library Management System ===")
        print("1. Add a book")
        print("2. Register a borrower")
        print("3. Check out a book")
        print("4. Return a book")
        print("5. Search by author")
        print("6. View overdue books")
        print("7. View popular genres")
        print("8. Quit")

        choice = input("\nChoose an option (1-8): ").strip()

        if choice == "1":
            menu_add_book()
        elif choice == "2":
            menu_add_borrower()
        elif choice == "3":
            menu_checkout()
        elif choice == "4":
            menu_return()
        elif choice == "5":
            menu_search_by_author()
        elif choice == "6":
            menu_overdue()
        elif choice == "7":
            menu_popular_genres()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
