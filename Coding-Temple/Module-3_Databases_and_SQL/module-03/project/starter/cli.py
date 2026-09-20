"""
Module 3 Project: Library Management System
cli.py — Command-line interface
"""

from library_system import (
    init_db, add_author, add_book, add_member,
    checkout_book, return_book, find_books_by_author, get_all_books,
    get_overdue_books, get_popular_genres, get_available_books, 
    search_books_by_title, update_member_email, delete_book, 
    delete_member, list_member_borrowings, engine, Session, Author
)

def menu_add_book():
    title = input("Please enter the title: ").strip()
    isbn = input("Please enter the ISBN: ").strip()
    author_name = input("Please enter the author's name: ").strip()
    
    with Session(engine) as session:
        author = session.query(Author).filter(Author.name.ilike(author_name)).first()
        author_id = author.id if author else None

    if not author_id:
        new_author = add_author(name=author_name)
        author_id = new_author.id
    
    try:
        year = int(input("Enter the published year: "))
    except ValueError:
        print("Invalid year input. Canceled.")
        return

    genres_input = input("Enter the book genre (comma-separated): ").strip()
    genres = [g.strip() for g in genres_input.split(",")] if genres_input else []
    
    try:
        book = add_book(title=title, isbn=isbn, author_ids=author_id, published_year=year, genre_names=genres)
        print(f"'{book.title}' has been added.")
    except Exception as e:
        print(f"Failed to add book: {e}")

def menu_list_all_books():
    books = get_all_books()
    if not books: 
        print("No books in the library system.")
    else:
        print("\n--- All Books ---")
        for b in books: 
            authors = ", ".join([a.name for a in b.author]) if b.author else "Unknown"
            print(f"ID {b.id}: '{b.title}' by {authors} (ISBN: {b.isbn}, Copies: {b.available_copies})")

def menu_add_borrower():
    name = input("Please enter your name: ").strip()
    email = input("Please enter your email address: ").strip()
    phone = input("Please enter your phone: ").strip()
    
    try:
        member = add_member(name=name, email=email, phone=phone or None)
        print(f"Member '{member.name}' has been added.")
    except Exception as e:
        print(f"Failed to add member: {e}")

def menu_checkout():
    available_books = get_available_books()
    if not available_books:
        print("No books are currently available for checkout.")
        return
    
    print("\n--- Available Books ---")
    for book in available_books: 
        print(f"ID {book['id']}: {book['title']} ({book['copies']} copies available)")
        
    try: 
        book_id = int(input("Enter the book ID: "))
        member_id = int(input("Enter the member ID: "))
        results = checkout_book(book_id=book_id, member_id=member_id)  
        print(f"Checkout completed successfully (Checkout ID: {results.id}).")
    except ValueError as e: 
        print(f"Checkout failed: {e}")

def menu_return():
    try:
        checkout_id = int(input("Please enter the checkout ID: "))
        results = return_book(checkout_id=checkout_id)
        print(f"Checkout ID {results.id} has been successfully returned.")
    except (ValueError, Exception) as e:
        print(f"Error returning book: {e}")

def menu_search_by_title():
    title_search = input("Please enter a title to search for: ").strip()
    results = search_books_by_title(title_search)
    if not results: 
        print("No books found matching that title.")
    else:
        for book in results: 
            print(f"- ID {book.id}: {book.title}")

def menu_member_borrowings():
    try: 
        member_id = int(input("Please enter the member ID: "))
    except ValueError: 
        print("Invalid member ID.")
        return 
    
    results = list_member_borrowings(member_id=member_id)
    if not results: 
        print("No active borrowings found for this member.")
    else:
        for result in results: 
            book_title = result.books.title if result.books else f"Book ID {result.book_id}"
            print(f"Checkout ID: {result.id} | Book: {book_title} | Due date: {result.due_date}")

def menu_update_member_email(): 
    try: 
        member_id = int(input("Enter Member ID: "))
        new_email = input("Enter new email: ").strip()
        updated = update_member_email(member_id, new_email)
        if updated:
            print(f"Updated email for {updated.name}: {updated.email}")
        else:
            print("Member not found.")
    except ValueError as e: 
        print(f"Update failed: {e}")

def menu_delete_book(): 
    try: 
        book_id = int(input("Enter Book ID to delete: "))
        if delete_book(book_id):
            print("Book deleted successfully.")
        else: 
            print("Could not delete book (active checkout exists or invalid ID).")
    except ValueError: 
        print("Invalid ID.")

def menu_delete_member():
    try:
        member_id = int(input("Enter Member ID to delete: "))
        if delete_member(member_id):
            print("Member deleted successfully.")
        else:
            print("Could not delete member (active checkout exists or invalid ID).")
    except ValueError: 
        print("Invalid ID.")

def menu_search_by_author():
    author_name = input("Please enter the author's name: ").strip()
    results = find_books_by_author(author_name=author_name)
    if not results: 
        print("No books found for that author.")
    else: 
        for book in results: 
            print(f"- ID {book.id}: {book.title}")

def menu_overdue():
    results = get_overdue_books()
    if not results: 
        print("No books are currently overdue.")
    else:
        for result in results: 
            book_title = result.books.title if result.books else f"Book ID {result.book_id}"
            member_name = result.members.name if result.members else f"Member ID {result.member_id}"
            print(f"Checkout ID: {result.id} | Book: {book_title} | Borrowed by: {member_name} | Due: {result.due_date}")

def menu_popular_genres():
    results = get_popular_genres()
    if not results: 
        print("No genre statistics available yet.")
    else:
        for genre in results: 
            print(f"Genre: {genre['name']} ({genre['count']} checkouts)")

def main():
    init_db()

    while True:
        print("\n=== Library Management System ===")
        print("1. Add a book")
        print("2. Register a borrower")
        print("3. Check out a book")
        print("4. Return a book")
        print("5. List all books")
        print("6. Search books by title")
        print("7. Search books by author")
        print("8. View Member's borrowings")
        print("9. View Popular Genres")
        print("10. View Overdue Books")
        print("11. Update member email")
        print("12. Delete a book")
        print("13. Delete a member")
        print("14. Quit")

        choice = input("\nChoose an option (1-14): ").strip()

        if choice == "1":
            menu_add_book()
        elif choice == "2":
            menu_add_borrower()
        elif choice == "3":
            menu_checkout()
        elif choice == "4":
            menu_return()
        elif choice == "5":
            menu_list_all_books()
        elif choice == "6":
            menu_search_by_title()
        elif choice == "7":
            menu_search_by_author()
        elif choice == "8":
            menu_member_borrowings() 
        elif choice == "9":
            menu_popular_genres()
        elif choice == "10":
            menu_overdue()
        elif choice == "11": 
            menu_update_member_email()
        elif choice == "12":
            menu_delete_book()
        elif choice == "13":
            menu_delete_member()
        elif choice == "14":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-14.")

if __name__ == "__main__":
    main()