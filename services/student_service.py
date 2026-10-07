import csv
import logging
from pathlib import Path

from models.student import Student
from utils.input_helper import InputHelper


class StudentService:
    def __init__(self, path="data/students.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.students = []
        self._load()

    def _load(self):
        import json
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.students = [Student.from_dict(item) for item in raw]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            logging.exception("Could not load student data")
            raise ValueError("Student data file is corrupted.") from exc

    def _save(self):
        import json
        self.path.write_text(
            json.dumps([s.to_dict() for s in self.students], indent=4),
            encoding="utf-8"
        )

    def _find(self, student_id):
        return next(
            (s for s in self.students if s.student_id.lower() == student_id.lower()),
            None
        )

    def add_student(self):
        print("\n--- Add Student ---")
        sid = InputHelper.get_non_empty("Student ID: ")
        if self._find(sid):
            raise ValueError("Student ID already exists.")

        name = InputHelper.get_name("Name: ")
        age = InputHelper.get_int("Age (10-100): ", 10, 100)
        course = InputHelper.get_non_empty("Course: ")
        email = InputHelper.get_email("Email: ")
        marks = InputHelper.get_float("Marks (0-100): ", 0, 100)

        student = Student(sid, name, age, course, email, marks)
        self.students.append(student)
        self._save()
        logging.info("Added student %s", sid)
        print("Student added successfully.")

    def display_students(self, students=None):
        students = self.students if students is None else students
        if not students:
            print("\nNo students found.")
            return

        print("\n" + "-" * 92)
        print(f"{'ID':<10}{'Name':<22}{'Age':<6}{'Course':<18}{'Marks':<9}{'Email':<25}")
        print("-" * 92)
        for s in students:
            print(f"{s.student_id:<10}{s.name:<22}{s.age:<6}{s.course:<18}"
                  f"{s.marks:<9.2f}{s.email:<25}")
        print("-" * 92)

    def search_students(self):
        term = InputHelper.get_non_empty("Search by ID/name/course/email: ").lower()
        results = [
            s for s in self.students
            if term in s.student_id.lower()
            or term in s.name.lower()
            or term in s.course.lower()
            or term in s.email.lower()
        ]
        self.display_students(results)

    def update_student(self):
        sid = InputHelper.get_non_empty("Enter Student ID to update: ")
        student = self._find(sid)
        if not student:
            print("Student not found.")
            return

        print("Press Enter to keep the current value.")
        name = input(f"Name [{student.name}]: ").strip() or student.name
        age = InputHelper.get_optional_int(f"Age [{student.age}]: ", 10, 100, student.age)
        course = input(f"Course [{student.course}]: ").strip() or student.course
        email = InputHelper.get_optional_email(f"Email [{student.email}]: ", student.email)
        marks = InputHelper.get_optional_float(
            f"Marks [{student.marks:.2f}]: ", 0, 100, student.marks
        )

        student.name, student.age, student.course = name, age, course
        student.email, student.marks = email, marks
        self._save()
        logging.info("Updated student %s", sid)
        print("Student updated successfully.")

    def delete_student(self):
        sid = InputHelper.get_non_empty("Enter Student ID to delete: ")
        student = self._find(sid)
        if not student:
            print("Student not found.")
            return

        confirm = input(f"Delete {student.name}? (y/n): ").strip().lower()
        if confirm == "y":
            self.students.remove(student)
            self._save()
            logging.info("Deleted student %s", sid)
            print("Student deleted successfully.")
        else:
            print("Deletion cancelled.")

    def sort_students(self):
        if not self.students:
            print("No students found.")
            return
        print("\n1. Name ascending\n2. Name descending\n3. Marks ascending\n4. Marks descending")
        choice = InputHelper.get_choice("Choose: ", 1, 4)
        if choice == 1:
            result = sorted(self.students, key=lambda s: s.name.lower())
        elif choice == 2:
            result = sorted(self.students, key=lambda s: s.name.lower(), reverse=True)
        elif choice == 3:
            result = sorted(self.students, key=lambda s: s.marks)
        else:
            result = sorted(self.students, key=lambda s: s.marks, reverse=True)
        self.display_students(result)

    def export_csv(self, path="exports/students.csv"):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["student_id", "name", "age", "course", "email", "marks"]
            )
            writer.writeheader()
            for student in self.students:
                writer.writerow(student.to_dict())
        print(f"CSV exported to {path}")

    def import_csv(self, path="exports/students.csv"):
        path = Path(path)
        if not path.exists():
            print(f"File not found: {path}")
            return

        added = 0
        with path.open("r", newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                try:
                    if self._find(row["student_id"]):
                        continue
                    student = Student.from_dict(row)
                    self.students.append(student)
                    added += 1
                except (KeyError, ValueError, TypeError):
                    logging.warning("Skipped invalid CSV row: %s", row)

        self._save()
        print(f"Imported {added} new student(s).")
