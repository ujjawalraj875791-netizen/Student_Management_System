# Library Management System

An intermediate-level **Python + SQLite** command-line Library Management System.

## Features

- Add and maintain book records
- Add and maintain library member records
- Issue books with a configurable due date
- Return books
- Automatic late fine calculation
- Search books by title or author
- Show all, available, and currently issued books
- Active loan/overdue report
- Complete loan history
- SQLite database persistence
- Backup and restore database
- Input validation and custom exceptions
- Multi-file modular structure

## Technologies

- Python 3.10+
- SQLite (`sqlite3`, built into Python)
- Standard library only — no external packages required

## Project structure

```text
library_management_system/
│
├── main.py
├── README.md
├── backups/
│
└── library/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── services.py
    └── ui.py
```

The `data/` folder and `library.db` file are created automatically the first time the program runs.

## Run

Open a terminal in the project folder:

```bash
python main.py
```

On Windows, if `python` does not work:

```bash
py main.py
```

## Default rules

- Default loan period: **14 days**
- Fine: **₹5 per late day**
- Both can be changed in `library/config.py`.

## How the system works

### Books
Each book has:
- ID
- title
- author
- ISBN
- category
- total copies
- available copies

### Members
Each member has:
- ID
- name
- email
- phone

### Loans
Each issue creates a loan record containing:
- book
- member
- issue date
- due date
- return date
- fine
- status

When a book is issued, `available_copies` decreases by 1.

When returned, `available_copies` increases by 1 and the fine is calculated from the number of days after the due date.

## Important learning concepts

This project is designed to practice:

1. Classes and objects
2. Modules and packages
3. Functions
4. Exception handling
5. SQLite CRUD operations
6. SQL JOINs
7. Foreign keys
8. Date and time calculations
9. File paths
10. Backup/restore using file copying
11. Input validation
12. Separation of UI and business logic

## Suggested extensions

After understanding this version, you can add:

- Admin login/password hashing
- Book update/delete
- Member update/delete
- Maximum books per member
- Reservation/waiting list
- Fine payment tracking
- CSV/Excel report export
- GUI using Tkinter
- Web version using Flask/Django
- Role-based access: Admin/Librarian/Member
- Dashboard with statistics
