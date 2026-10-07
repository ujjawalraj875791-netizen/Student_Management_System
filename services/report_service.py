from utils.input_helper import InputHelper


class ReportService:
    def __init__(self, student_service):
        self.ss = student_service

    def menu(self):
        while True:
            print("""
--------------- REPORTS ---------------
1. Topper
2. Average marks
3. Pass/Fail summary
4. Course-wise summary
5. Individual student report
0. Back
----------------------------------------
""")
            choice = InputHelper.get_choice("Choose: ", 0, 5)

            if choice == 0:
                return
            if choice == 1:
                self.topper()
            elif choice == 2:
                self.average()
            elif choice == 3:
                self.pass_fail()
            elif choice == 4:
                self.course_summary()
            elif choice == 5:
                self.student_report()

    def topper(self):
        if not self.ss.students:
            print("No students available.")
            return
        top = max(self.ss.students, key=lambda s: s.marks)
        print(f"\nTopper: {top.name} ({top.student_id}) - {top.marks:.2f}/100")

    def average(self):
        if not self.ss.students:
            print("No students available.")
            return
        avg = sum(s.marks for s in self.ss.students) / len(self.ss.students)
        print(f"\nAverage marks: {avg:.2f}/100")

    def pass_fail(self, pass_mark=40):
        passed = sum(s.marks >= pass_mark for s in self.ss.students)
        failed = len(self.ss.students) - passed
        print(f"\nPass mark: {pass_mark}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

    def course_summary(self):
        if not self.ss.students:
            print("No students available.")
            return
        courses = {}
        for s in self.ss.students:
            courses.setdefault(s.course, []).append(s.marks)

        print("\nCourse-wise summary:")
        for course, marks in sorted(courses.items()):
            print(f"{course:<20} Students: {len(marks):<4} Average: {sum(marks)/len(marks):.2f}")

    def student_report(self):
        sid = InputHelper.get_non_empty("Student ID: ")
        student = next(
            (s for s in self.ss.students if s.student_id.lower() == sid.lower()),
            None
        )
        if not student:
            print("Student not found.")
            return

        result = "PASS" if student.marks >= 40 else "FAIL"
        print(f"""
========== STUDENT REPORT ==========
ID      : {student.student_id}
Name    : {student.name}
Age     : {student.age}
Course  : {student.course}
Email   : {student.email}
Marks   : {student.marks:.2f}/100
Status  : {result}
====================================
""")
