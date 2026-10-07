from dataclasses import dataclass, asdict


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    course: str
    email: str
    marks: float

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=str(data["student_id"]),
            name=str(data["name"]),
            age=int(data["age"]),
            course=str(data["course"]),
            email=str(data["email"]),
            marks=float(data["marks"]),
        )
