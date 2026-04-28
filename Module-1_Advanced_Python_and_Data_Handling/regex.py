import re
records = [
    "Name: Alice Johnson | Email: alice.j@gmail.com | Phone: (555) 123-4567 | Joined: 01/15/2023",
    "Name: Bob Smith | Email: bob_smith@yahoo.com | Phone: 555.987.6543 | Joined: 03-22-2023",
    "Name: Charlie Brown | Email: charlie@outlook.com | Phone: 555 111 2222 | Joined: 2023/07/01",
    "Name: Diana Prince | Email: diana.prince@company.co.uk | Phone: (555)444-3333 | Joined: 11/30/2023",
]

# Write Python functions using re to:

# extract_names(records) - Return a list of names
def extract_name(records):
    return [name.strip() for name in re.findall(r"Name: ([^|]+)", records)]


# extract_emails(records) - Return a list of email addresses
def extract_emails(records):
    return re.findall(r"Email: ([\w.+_]+@[\w-]+\.[\w.]+)", records)
# normalize_phones(records) - Return all phone numbers in XXX-XXX-XXXX format
def normalize_phones(records):
    phones = re.findall(r"Phone: [\(\s]?(\d{3})[\)\.\s-]?(\d{3})[\.\s-]?(\d{4})", records)
    return [f"{area}-{prefix}-{line}" for area, prefix, line in phones]
    
# extract_dates(records) - Return all dates, regardless of format
def extract_dates(records): 
    return re.findall(r"Joined: (\d{2,4}[/-]?\d{2}[/-]?\d{2,4})", records)
# Bonus: Write a function that parses each record into a dictionary: {"name": ..., "email": ..., "phone": ..., "joined": ...}
def parse_records(record): 
        return{
            "Name": extract_name(record)[0],
            "Email": extract_emails(record)[0],
            "Phone": normalize_phones(record)[0],
            "Joined": extract_dates(record)[0]
        }

[parse_records(record) for record in records]