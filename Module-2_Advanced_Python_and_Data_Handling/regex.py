import re
records = [
    "Name: Alice Johnson | Email: alice.j@gmail.com | Phone: (555) 123-4567 | Joined: 01/15/2023",
    "Name: Bob Smith | Email: bob_smith@yahoo.com | Phone: 555.987.6543 | Joined: 03-22-2023",
    "Name: Charlie Brown | Email: charlie@outlook.com | Phone: 555 111 2222 | Joined: 2023/07/01",
    "Name: Diana Prince | Email: diana.prince@company.co.uk | Phone: (555)444-3333 | Joined: 11/30/2023",
]

# Write Python functions using re to:

# extract_names(records) - Return a list of names
def extract_names(records):
    return [name.strip() for record in records for name in re.findall(r"Name:\s+([^|]+)", record)]


# extract_emails(records) - Return a list of email addresses
def extract_emails(records):
    return [email.strip() for record in records for email in re.findall(r"Email: ([\w.+_]+@[\w-]+\.[\w.]+)", record)]
# normalize_phones(records) - Return all phone numbers in XXX-XXX-XXXX format
def normalize_phones(records):
    pattern = r"Phone: [\(\s]?(\d{3})[\)\.\s-]?(\d{3})[\.\s-]?(\d{4})"
    return [f"{area}-{prefix}-{line}" for record in records for area, prefix, line in re.findall(pattern, record)]
    
# extract_dates(records) - Return all dates, regardless of format
def extract_dates(records): 
    return [dates.strip() for record in records for dates in re.findall(r"Joined: (\d{2,4}[/-]?\d{2}[/-]?\d{2,4})", record)]
# Bonus: Write a function that parses each record into a dictionary: {"name": ..., "email": ..., "phone": ..., "joined": ...}
def parse_records(records): 
        names = extract_names(records)
        emails = extract_emails(records)
        phone = normalize_phones(records)
        dates = extract_dates(records)
        return [
             {"name": n, "email": e, "phone": p, "joined":d}
             for n, e, p, d in zip(names, emails, phone, dates)
        ]

# =============================================================================
# Print results
# =============================================================================

print("=" * 60)
print("extract_names()")
print("=" * 60)
for name in extract_names(records):
    print(f"  {name}")

print("\n" + "=" * 60)
print("extract_emails()")
print("=" * 60)
for email in extract_emails(records):
    print(f"  {email}")

print("\n" + "=" * 60)
print("normalize_phones()  →  XXX-XXX-XXXX")
print("=" * 60)
for phone in normalize_phones(records):
    print(f"  {phone}")

print("\n" + "=" * 60)
print("extract_dates()")
print("=" * 60)
for date in extract_dates(records):
    print(f"  {date}")

print("\n" + "=" * 60)
print("BONUS: parse_records()")
print("=" * 60)
for rec in parse_records(records):
    print(f"  {rec}")