import sqlite3
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE members(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT, 
               join_date TEXT)""")
cursor.execute("""CREATE TABLE books(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               title TEXT, 
               genre TEXT, 
               year_published INTEGER)""")
cursor.execute("""CREATE TABLE checkouts(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               member_id INTEGER, 
               book_id INTEGER, 
               checkout_date TEXT, 
               return_date TEXT NULL, 
               FOREIGN KEY (member_id) REFERENCES members(id), 
               FOREIGN KEY (book_id) REFERENCES books(id))""")

members = [
    (1, "Alice Morgan", "2022-03-15"),
    (2, "Ben Carter", "2021-11-02"),
    (3, "Clara Diaz", "2023-01-20"),
    (4, "David Kim", "2022-07-08"),
    (5, "Elena Russo", "2023-05-30")
]

books = [
    (1, "The Great Gatsby", "Fiction", 1925),
    (2, "To Kill a Mockingbird", "Fiction", 1960),
    (3, "1984", "Dystopia", 1949),
    (4, "Brave New World", "Dystopia", 1932),
    (5, "A Brief History of Time", "Non-Fiction", 1988),
    (6, "Sapiens", "Non-Fiction", 2011),
    (7, "Dune", "Sci-Fi", 1965),
    (8, "The Martian", "Sci-Fi", 2011)
]

checkouts = [
    (1, 1, 1, "2023-01-10", "2023-01-20"),
    (2, 1, 3, "2023-02-05", "2023-02-15"),
    (3, 1, 7, "2023-03-01", None),
    (4, 2, 2, "2023-01-15", "2023-01-25"),
    (5, 2, 4, "2023-02-10", "2023-02-20"),
    (6, 2, 6, "2023-03-05", "2023-03-15"),
    (7, 2, 8, "2023-04-01", None),
    (8, 3, 1, "2023-02-01", "2023-02-10"),
    (9, 3, 5, "2023-03-10", "2023-03-20"),
    (10, 3, 7, "2023-04-05", None),
    (11, 4, 2, "2023-01-20", "2023-01-30"),
    (12, 4, 3, "2023-02-15", "2023-02-25"),
    (13, 4, 6, "2023-03-15", "2023-03-25"),
    (14, 5, 1, "2023-02-20", "2023-03-01"),
    (15, 5, 4, "2023-03-20", "2023-04-01"),
    (16, 5, 8, "2023-04-10", None)
]

cursor.executemany("INSERT INTO members(id, name, join_date) VALUES (?, ? , ?)", members)

cursor.executemany("INSERT INTO books(id, title, genre, year_published) VALUES (?,?,?,?)", books)

cursor.executemany("INSERT INTO checkouts(id, member_id, book_id, checkout_date, return_date) VALUES (?,?,?,?,?)", checkouts)
connection.commit()

# How many books are in each genre? (GROUP BY)

cursor.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre")

for row in cursor.fetchall():
    print(f" Name: {row[0]} Count: {row[1]}")
# Which member has checked out the most books? (GROUP BY + ORDER BY + LIMIT)
cursor.execute("SELECT member_id, members.name, COUNT(*) FROM checkouts JOIN members ON checkouts.member_id = members.id GROUP BY member_id ORDER BY COUNT(*) DESC LIMIT 1")

for row in cursor.fetchall():
    print(f" Member: {row[0]} Name: {row[1]} Books Checked Out: {row[2]}")
# What is the average number of checkouts per member? (subquery or nested aggregation)
cursor.execute("SELECT AVG(checkout_count) FROM (SELECT COUNT(*) AS checkout_count FROM checkouts GROUP BY member_id)")

print(cursor.fetchall())
# Which genres have more than 3 checkouts? (GROUP BY + HAVING)
cursor.execute("SELECT books.genre FROM checkouts JOIN books ON books.id = checkouts.book_id GROUP BY genre HAVING COUNT(*) > 3")

print(cursor.fetchall())
# Which books have never been checked out? (subquery with NOT IN)
cursor.execute("SELECT title FROM books WHERE id NOT IN (SELECT book_id FROM checkouts) ")

print(cursor.fetchall())