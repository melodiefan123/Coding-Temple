import sqlite3

connection = sqlite3.connect("music.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""CREATE TABLE IF NOT EXISTS artists (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               genre TEXT)"""
               )

cursor.execute("""CREATE TABLE IF NOT EXISTS albums (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               year INTEGER,
               artist_id INTEGER, 
               FOREIGN KEY(artist_id) REFERENCES artists(id) ) 
               """
               )

artists=[
    ("Beyonce", "R&B"),
    ("Beyonce", "R&B"),
    ("new artist 1", "genre 1"),
    ("new artist 2", "genre 2"),

]
cursor.executemany("INSERT OR IGNORE INTO artists(name, genre) VALUES(?,?)", artists )
albums=[
    ("Lemonade", 2013, 1), 
    ("new album 1", 2024, 1),
    ("new album 2", 2025, 1),
    ("new album 3", 2025, 2),
    ("new album 4", 2025, 3)

]
cursor.executemany("INSERT INTO albums(title, year, artist_id) VALUES(?,?,?)", albums )

connection.commit()
print("\n Tables committed")

cursor.execute("SELECT artists.id, artists.name, artists.genre, albums.title, albums.year FROM artists JOIN albums ON artists.id = albums.artist_id")

for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Genre: {row[2]}, Album Title: {row[3]}, Year: {row[4]} ")
connection.close()
print("\n Connection closed ")

