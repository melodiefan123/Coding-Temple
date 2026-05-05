"""
seed_data.py — Populate the database with sample data for testing.
Run this AFTER implementing the models in library_system.py:
    python seed_data.py
"""

from library_system import init_db, add_author, add_book, add_member

def seed():
    init_db()
    print("Database initialized.")

    # Uncomment and expand once you've implemented the model functions:

    tolkien = add_author("J.R.R. Tolkien", "Author of The Lord of the Rings")
    austen  = add_author("Jane Austen")
    morrison = add_author("Toni Morrison")
    fitzgerald = add_author("F.Scott Fitzgerald")
    add_book("The Hobbit", "978-0618260300", tolkien.id, 1937, ["Fantasy", "Adventure"])
    add_book("1984", "978-0451524935", morrison.id, 1949, ["Dystopian", "Fiction"])
    add_book("Beloved", "978-1400033416", morrison.id, 1987,["Historical","Fiction"])
    add_book("The Great Gatsby", "978-0743273565", fitzgerald.id, 1925["Classic", "Fiction"])
    add_book("Pride and Prejudice", "978-0141439518", austen.id, 1813, ["Fiction", "Romance"])
    add_member("Alice Chen", "alice@example.com", "555-0101")
    add_member("Bob Martinez", "bob@example.com")
    add_member("Carol White", "carol@example.com")
    add_member("David Kim", "david@example.com")

    print("Seed complete! (Uncomment the lines above after implementing your models.)")

if __name__ == "__main__":
    seed()
