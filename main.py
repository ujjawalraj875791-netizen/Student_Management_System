from services.auth_service import AuthService
from services.student_service import StudentService
from services.report_service import ReportService
from utils.input_helper import InputHelper
import logging
from pathlib import Path


Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():
    #cleared
    auth = AuthService()
    if not auth.login():
        print("\nToo many failed attempts. Exiting.")
        return

    student_service = StudentService()
    report_service = ReportService(student_service)
    menu = InputHelper()

    while True:
        print("""
========== STUDENT MANAGEMENT SYSTEM ==========
1. Add student
2. View all students
3. Search student
4. Update student
5. Delete student
6. Sort students
7. Reports
8. Export students to CSV
9. Import students from CSV
0. Exit
===============================================
""")
        choice = menu.get_choice("Enter choice: ", 0, 9)

        try:
            if choice == 1:
                student_service.add_student()
            elif choice == 2:
                student_service.display_students()
            elif choice == 3:
                student_service.search_students()
            elif choice == 4:
                student_service.update_student()
            elif choice == 5:
                student_service.delete_student()
            elif choice == 6:
                student_service.sort_students()
            elif choice == 7:
                report_service.menu()
            elif choice == 8:
                student_service.export_csv()
            elif choice == 9:
                student_service.import_csv()
            else:
                print("Thank you for using Student Management System.")
                break
        except Exception as exc:
            print(f"Operation failed: {exc}")


if __name__ == "__main__":
    main()
