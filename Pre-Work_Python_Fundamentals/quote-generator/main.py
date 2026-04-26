import random 

quotes = [
    ('We are what we repeatedly do. Excellence, then, is not an act, but a habit.”', 'Aristotle'),
    ('Not all those who wander are lost.', 'J. R. R. Tolkien'),
    ('The only way to do great work is to love what you do.', 'Steve Jobs'),
    ('In the middle of difficulty lies opportunity.', 'Albert Einstein'),
    ('It is never too late to be what you might have been.','George Eliot'),
    ('Happiness depends upon ourselves.', 'Aristotle'),
    ('Tell me and I forget. Teach me and I remember. Involve me and I learn.', 'Benjamin Franklin'), 
    ('All we have to decide is what to do with the time that is given us.', 'J. R. R. Tolkien'),
    ('Do one thing every day that scares you.', 'Eleanor Roosevelt'),
    ('The unexamined life is not worth living.', 'Socrates')]

def random_quotes():
    random_quote = random.choice(quotes)
    text = random_quote[0]
    author = random_quote[1]
    print("=== Quote of the day ===")
    print(f"{text} — {author}")



random_quotes()