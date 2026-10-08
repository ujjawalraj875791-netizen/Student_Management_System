from datetime import date, timedelta
from pathlib import Path
import shutil
import sqlite3

from .config import BACKUP_DIR, DB_PATH, DEFAULT_LOAN_DAYS, FINE_PER_DAY
from .database import get_connection

class LibraryError(Exception):
    pass

class LibraryService:
    def add_book(self, title, author, isbn, category, copies):
        if copies < 1:
            raise LibraryError("Copies must be at least 1.")
        try:
            with get_connection() as conn:
                conn.execute(
                    """INSERT INTO books(title, author, isbn, category, total_copies, available_copies)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (title, author, isbn or None, category or None, copies, copies)
                )
        except sqlite3.IntegrityError as exc:
            raise LibraryError("ISBN already exists.") from exc

    def add_member(self, name, email, phone):
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO members(name, email, phone) VALUES (?, ?, ?)",
                    (name, email or None, phone or None)
                )
        except sqlite3.IntegrityError as exc:
            raise LibraryError("Email already exists.") from exc

    def list_books(self, mode="all"):
        query = "SELECT * FROM books ORDER BY title"
        params = ()
        if mode == "available":
            query = "SELECT * FROM books WHERE available_copies > 0 ORDER BY title"
        elif mode == "issued":
            query = """
                SELECT b.id, b.title, b.author, b.isbn, b.category,
                       b.total_copies, b.available_copies
                FROM books b
                WHERE b.available_copies < b.total_copies
                ORDER BY b.title
            """
        with get_connection() as conn:
            return conn.execute(query, params).fetchall()

    def list_members(self):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM members ORDER BY name").fetchall()

    def search_books(self, term):
        like = f"%{term}%"
        with get_connection() as conn:
            return conn.execute(
                """SELECT * FROM books
                   WHERE title LIKE ? OR author LIKE ?
                   ORDER BY title""",
                (like, like)
            ).fetchall()

    def issue_book(self, book_id, member_id, loan_days=DEFAULT_LOAN_DAYS):
        today = date.today()
        due = today + timedelta(days=loan_days)
        with get_connection() as conn:
            book = conn.execute(
                "SELECT * FROM books WHERE id = ?", (book_id,)
            ).fetchone()
            member = conn.execute(
                "SELECT * FROM members WHERE id = ?", (member_id,)
            ).fetchone()

            if not book:
                raise LibraryError("Book not found.")
            if not member:
                raise LibraryError("Member not found.")
            if book["available_copies"] <= 0:
                raise LibraryError("No available copy of this book.")

            # Prevent the same member from holding the same book twice.
            active = conn.execute(
                """SELECT id FROM loans
                   WHERE book_id = ? AND member_id = ? AND status = 'ISSUED'""",
                (book_id, member_id)
            ).fetchone()
            if active:
                raise LibraryError("This member already has this book issued.")

            conn.execute(
                """INSERT INTO loans(book_id, member_id, issue_date, due_date)
                   VALUES (?, ?, ?, ?)""",
                (book_id, member_id, today.isoformat(), due.isoformat())
            )
            conn.execute(
                "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?",
                (book_id,)
            )
        return due

    def return_book(self, loan_id):
        today = date.today()
        with get_connection() as conn:
            loan = conn.execute(
                "SELECT * FROM loans WHERE id = ? AND status = 'ISSUED'",
                (loan_id,)
            ).fetchone()
            if not loan:
                raise LibraryError("Active loan not found.")

            due = date.fromisoformat(loan["due_date"])
            late_days = max((today - due).days, 0)
            fine = late_days * FINE_PER_DAY

            conn.execute(
                """UPDATE loans
                   SET return_date = ?, fine = ?, status = 'RETURNED'
                   WHERE id = ?""",
                (today.isoformat(), fine, loan_id)
            )
            conn.execute(
                "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?",
                (loan["book_id"],)
            )
        return fine, late_days

    def active_loans(self):
        with get_connection() as conn:
            return conn.execute(
                """SELECT l.*, b.title, b.author, m.name AS member_name
                   FROM loans l
                   JOIN books b ON b.id = l.book_id
                   JOIN members m ON m.id = l.member_id
                   WHERE l.status = 'ISSUED'
                   ORDER BY l.due_date"""
            ).fetchall()

    def loan_history(self):
        with get_connection() as conn:
            return conn.execute(
                """SELECT l.*, b.title, m.name AS member_name
                   FROM loans l
                   JOIN books b ON b.id = l.book_id
                   JOIN members m ON m.id = l.member_id
                   ORDER BY l.issue_date DESC"""
            ).fetchall()

    def backup(self):
        if not DB_PATH.exists():
            raise LibraryError("Database does not exist yet.")
        filename = BACKUP_DIR / f"library_backup_{date.today().isoformat()}.db"
        # Add suffix if today's backup already exists.
        counter = 1
        candidate = filename
        while candidate.exists():
            candidate = BACKUP_DIR / f"library_backup_{date.today().isoformat()}_{counter}.db"
            counter += 1
        shutil.copy2(DB_PATH, candidate)
        return candidate

    def restore(self, backup_path):
        source = Path(backup_path)
        if not source.exists():
            raise LibraryError("Backup file not found.")
        if source.suffix.lower() != ".db":
            raise LibraryError("Please select a .db backup file.")

        # Validate that it is a readable SQLite database.
        try:
            conn = sqlite3.connect(source)
            conn.execute("PRAGMA integrity_check").fetchone()
            conn.close()
        except sqlite3.Error as exc:
            raise LibraryError("Invalid SQLite backup.") from exc

        shutil.copy2(source, DB_PATH)
