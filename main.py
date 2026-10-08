from pathlib import Path
from library.database import initialize_database
from library.services import LibraryError, LibraryService
from library.ui import (
    header, pause, get_nonempty, get_int,
    show_books, show_members, show_active_loans, show_history
)
from library.config import BACKUP_DIR, DEFAULT_LOAN_DAYS, FINE_PER_DAY

service = LibraryService()

def add_book():
    header("ADD BOOK")
    title = get_nonempty("Title: ")
    author = get_nonempty("Author: ")
    isbn = input("ISBN (optional): ").strip()
    category = input("Category (optional): ").strip()
    copies = get_int("Number of copies: ", 1)
    try:
        service.add_book(title, author, isbn, category, copies)
        print("Book added successfully.")
    except LibraryError as e:
        print(f"Error: {e}")
    pause()

def add_member():
    header("ADD MEMBER")
    name = get_nonempty("Name: ")
    email = input("Email (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    try:
        service.add_member(name, email, phone)
        print("Member added successfully.")
    except LibraryError as e:
        print(f"Error: {e}")
    pause()

def issue_book():
    header("ISSUE BOOK")
    print("Available books:")
    show_books(service.list_books("available"))
    book_id = get_int("Book ID: ", 1)

    print("\nMembers:")
    show_members(service.list_members())
    member_id = get_int("Member ID: ", 1)

    days = input(f"Loan period in days [{DEFAULT_LOAN_DAYS}]: ").strip()
    loan_days = int(days) if days else DEFAULT_LOAN_DAYS
    if loan_days < 1:
        print("Loan period must be positive.")
        pause()
        return

    try:
        due = service.issue_book(book_id, member_id, loan_days)
        print(f"Book issued successfully. Due date: {due.isoformat()}")
    except (LibraryError, ValueError) as e:
        print(f"Error: {e}")
    pause()

def return_book():
    header("RETURN BOOK")
    loans = service.active_loans()
    show_active_loans(loans)
    if not loans:
        pause()
        return

    loan_id = get_int("Loan ID to return: ", 1)
    try:
        fine, late_days = service.return_book(loan_id)
        print(f"Returned successfully.")
        print(f"Late by: {late_days} day(s)")
        print(f"Fine: ₹{fine:.2f}")
    except LibraryError as e:
        print(f"Error: {e}")
    pause()

def search_books():
    header("SEARCH BOOKS")
    term = get_nonempty("Enter title or author: ")
    show_books(service.search_books(term))
    pause()

def books_menu():
    while True:
        header("BOOKS")
        print("1. Add book")
        print("2. Show all books")
        print("3. Show available books")
        print("4. Show books with issued copies")
        print("5. Search by title/author")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            header("ALL BOOKS"); show_books(service.list_books()); pause()
        elif choice == "3":
            header("AVAILABLE BOOKS"); show_books(service.list_books("available")); pause()
        elif choice == "4":
            header("ISSUED BOOKS"); show_books(service.list_books("issued")); pause()
        elif choice == "5":
            search_books()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def members_menu():
    while True:
        header("MEMBERS")
        print("1. Add member")
        print("2. Show members")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_member()
        elif choice == "2":
            header("MEMBERS"); show_members(service.list_members()); pause()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def reports_menu():
    while True:
        header("REPORTS")
        print("1. Active loans / overdue")
        print("2. Complete loan history")
        print("3. Available books")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            header("ACTIVE LOANS")
            show_active_loans(service.active_loans())
            pause()
        elif choice == "2":
            header("LOAN HISTORY")
            show_history(service.loan_history())
            pause()
        elif choice == "3":
            header("AVAILABLE BOOKS")
            show_books(service.list_books("available"))
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def backup_restore_menu():
    while True:
        header("BACKUP & RESTORE")
        print(f"Backup folder: {BACKUP_DIR}")
        print("1. Create backup")
        print("2. Restore backup")
        print("3. List backups")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            try:
                path = service.backup()
                print(f"Backup created: {path}")
            except LibraryError as e:
                print(f"Error: {e}")
            pause()
        elif choice == "2":
            backups = sorted(BACKUP_DIR.glob("*.db"))
            if not backups:
                print("No backups available.")
                pause()
                continue
            for i, path in enumerate(backups, 1):
                print(f"{i}. {path.name}")
            idx = get_int("Select backup number: ", 1)
            if idx > len(backups):
                print("Invalid backup number.")
            else:
                confirm = input("Restore this backup? This will replace current data. (yes/no): ").strip().lower()
                if confirm == "yes":
                    try:
                        service.restore(backups[idx - 1])
                        print("Database restored successfully.")
                    except LibraryError as e:
                        print(f"Error: {e}")
                else:
                    print("Restore cancelled.")
            pause()
        elif choice == "3":
            backups = sorted(BACKUP_DIR.glob("*.db"))
            if backups:
                for path in backups:
                    print(path.name)
            else:
                print("No backups found.")
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def seed_demo_data():
    if service.list_books() or service.list_members():
        return
    try:
        service.add_book("Python Programming", "Mark Lutz", "ISBN-PY-001", "Programming", 3)
        service.add_book("Clean Code", "Robert C. Martin", "ISBN-CC-001", "Programming", 2)
        service.add_book("Database System Concepts", "Korth", "ISBN-DB-001", "Database", 2)
        service.add_member("Aman Sharma", "aman@example.com", "9876543210")
        service.add_member("Priya Singh", "priya@example.com", "9876501234")
    except LibraryError:
        pass

def main():
    initialize_database()
    # Uncomment the next line if you want sample records on a fresh database.
    # seed_demo_data()

    while True:
        header("LIBRARY MANAGEMENT SYSTEM")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Reports")
        print("6. Backup & Restore")
        print("0. Exit")
        print(f"\nFine rate: ₹{FINE_PER_DAY:.2f}/day | Default loan: {DEFAULT_LOAN_DAYS} days")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            books_menu()
        elif choice == "2":
            members_menu()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            reports_menu()
        elif choice == "6":
            backup_restore_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
