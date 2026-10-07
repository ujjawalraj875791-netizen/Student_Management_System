import json
from pathlib import Path

from models.student import Student


def test_student_to_dict():
    student = Student("S100", "Test User", 20, "BCA", "test@example.com", 80)
    data = student.to_dict()
    assert data["student_id"] == "S100"
    assert data["marks"] == 80


def test_student_from_dict():
    data = {
        "student_id": "S101",
        "name": "Test User",
        "age": "21",
        "course": "MCA",
        "email": "test@example.com",
        "marks": "91.5"
    }
    student = Student.from_dict(data)
    assert student.age == 21
    assert student.marks == 91.5
