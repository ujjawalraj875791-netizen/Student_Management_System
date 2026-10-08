from datetime import date

def line(char="-", width=90):
    print(char * width)

def pause():
    input("\nPress Enter to continue...")

def header(title):
    print("\n")
    line("=")
    print(title.center(90))
    line("=")

def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")

def get_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Enter a valid integer.")

def show_books(rows):
    if not rows:
        print("No books found.")
        return
    print(f"{'ID':<4} {'Title':<28} {'Author':<22} {'Category':<15} {'Available':<10}")
    line()
    for r in rows:
        print(f"{r['id']:<4} {r['title'][:27]:<28} {r['author'][:21]:<22} "
              f"{(r['category'] or '-')[:14]:<15} {r['available_copies']}/{r['total_copies']:<10}")

def show_members(rows):
    if not rows:
        print("No members found.")
        return
    print(f"{'ID':<4} {'Name':<25} {'Email':<30} {'Phone':<15}")
    line()
    for r in rows:
        print(f"{r['id']:<4} {r['name'][:24]:<25} {(r['email'] or '-')[:29]:<30} {(r['phone'] or '-')[:14]:<15}")

def show_active_loans(rows):
    if not rows:
        print("No active issued books.")
        return
    print(f"{'Loan':<5} {'Book':<25} {'Member':<20} {'Due':<12} {'Status':<10}")
    line()
    for r in rows:
        overdue = date.today() > date.fromisoformat(r["due_date"])
        status = "OVERDUE" if overdue else "ISSUED"
        print(f"{r['id']:<5} {r['title'][:24]:<25} {r['member_name'][:19]:<20} "
              f"{r['due_date']:<12} {status:<10}")

def show_history(rows):
    if not rows:
        print("No loan history.")
        return
    print(f"{'Loan':<5} {'Book':<24} {'Member':<18} {'Issue':<12} {'Return':<12} {'Fine':<8}")
    line()
    for r in rows:
        print(f"{r['id']:<5} {r['title'][:23]:<24} {r['member_name'][:17]:<18} "
              f"{r['issue_date']:<12} {(r['return_date'] or '-'):<12} ₹{r['fine']:<7.2f}")
