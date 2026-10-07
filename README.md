# Student Management System

An intermediate-level Python CLI project for managing student records.

## Features

- Admin login authentication
- Add, update, delete and search students
- JSON persistence
- CSV import/export
- Sort by name or marks
- Topper report
- Average marks
- Pass/fail summary
- Course-wise summary
- Individual student report
- Input validation
- Exception handling
- Application logging
- Modular OOP-based architecture

## Requirements

- Python 3.10+
- No external packages are required.

## Run

From the project directory:

```bash
python main.py
```

## Demo login

```text
Username: admin
Password: admin123
```

Change the demo password before using the application for anything real.

## Project structure

```text
student_management_system/
│
├── main.py
├── models/
│   └── student.py
├── services/
│   ├── auth_service.py
│   ├── student_service.py
│   └── report_service.py
├── utils/
│   └── input_helper.py
├── data/
│   ├── students.json
│   └── users.json
├── exports/
│   └── students.csv
├── logs/
└── tests/
```

## Data design

Students are stored as JSON records. CSV is available for export/import.

Student fields:

- student_id
- name
- age
- course
- email
- marks

## Important concepts demonstrated

- Classes and dataclasses
- Separation of concerns
- CRUD operations
- JSON and CSV
- Regular expressions
- Exception handling
- Logging
- Password hashing
- Sorting with `lambda`
- List comprehensions
- `pathlib`
- Date-independent report calculations

## Suggested future upgrades

1. SQLite/MySQL database
2. Multiple admin/teacher roles
3. Password change screen
4. Attendance module
5. Subject-wise marks
6. PDF report generation
7. Tkinter GUI
8. Flask web application
9. Unit tests with pytest
10. Backup/restore snapshots
