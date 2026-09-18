import sqlite3
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE departments(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT, 
               location TEXT UNIQUE)""")
cursor.execute("""CREATE TABLE employees(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT, 
               role TEXT, 
               salary INTEGER, 
               department_id INTEGER, 
               FOREIGN KEY (department_id) REFERENCES departments(id))""")
cursor.execute("""CREATE TABLE projects(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               title TEXT, 
               employee_id INTEGER, 
               FOREIGN KEY (employee_id) REFERENCES employees(id))""")

departments = [
    (1, "department 1", "first floor"),
    (2, "department 2", "second floor"),
    (3, "department 3", "third floor")
    ]

employees = [
    (1, "employee 1", "HR", 80000, 1), 
    (2, "employee 2", "IT", 90000, 1),
    (3, "employee 3", "Operations", 100000, 2),
    (4, "employee 4", "Accounts", 80000, 2),
    (5, "employee 5", "Executives", 130000, 3),
    (6, "employee 6", "C-Suite Execs", 180000, 3),
    (7, "employee 7", "Customer Support", 180000, 1),
    (8, "employee 8", "Production", 180000, 2)
]

projects = [
    (1, "Project 1", 2), 
    (2, "Project 2", 3), 
    (3, "Project 3", 1), 
    (4, "Project 4", 2)
]

cursor.executemany("INSERT INTO departments(id, name, location) VALUES (?, ? , ?)", departments)

cursor.executemany("INSERT INTO employees(id, name, role, salary, department_id) VALUES (?,?,?,?,?)", employees)

cursor.executemany("INSERT INTO projects(id, title, employee_id) VALUES (?,?,?)", projects)
connection.commit()


# Query 1: List all employees with their department name (INNER JOIN)
cursor.execute("SELECT name, role, departments.name FROM employees INNER JOIN departments ON departments.id = employees.department_id ")

for row in cursor.fetchall():
    print(f" Name: {row[0]} Role: {row[1]} Department: {row[2]}")
# Query 2: List all departments, even those with no employees (LEFT JOIN)

cursor.execute("SELECT departments.name, employees.name FROM departments LEFT JOIN employees ON departments.id = employees.department_id")
for row in cursor.fetchall():
    print(f"Department: {row[0]} Employee: {row[1]}")
# Query 3: List all employees and the projects they lead, including employees who don't lead any project (LEFT JOIN)
cursor.execute("SELECT projects.title, employees.name FROM employees LEFT JOIN projects ON employees.id=projects.employee_id")

for row in cursor.fetchall():
    print(f" Employee: {row[0]} Project: {row[1]} ")
# Query 4: Find employees who don't lead any project (LEFT JOIN + IS NULL)
cursor.execute("SELECT employees.name FROM employees LEFT JOIN projects ON employees.id=projects.employee_id WHERE projects.employee_id IS NULL")

for row in cursor.fetchall():
    print(f" Employees who don't lead any projects: {row[0]} ")
# Query 5: List all projects with the project lead's name AND their department name (requires joining 3 tables)
cursor.execute("SELECT employees.name, projects.title, departments.name FROM projects LEFT JOIN employees ON employees.id=projects.employee_id LEFT JOIN departments ON departments.id = employees.department_id")

for row in cursor.fetchall():
    print(f" Employee: {row[0]} Project: {row[1]} Department: {row[2]} ")