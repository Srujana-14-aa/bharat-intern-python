# bharat-intern-python
Python Development Internship Projects
"""
==============================================================
 LIBRARY MANAGEMENT SYSTEM
==============================================================
A console-based Library Management System built with Python.

Features:
    - Book Management (Add / View / Search)
    - Member Management (Register / View)
    - Issue & Return Books
    - Borrowing History
    - Reports (Book / Member / Transaction)
    - Persistent storage using JSON files
    - Robust error handling

Author : (Your Name)
Tech   : Python 3.x, json, csv, datetime, os
==============================================================
"""

import json
import csv
import os
from datetime import datetime, date

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")

DATE_FORMAT = "%Y-%m-%d"


# --------------------------------------------------------------------------
# UTILITY / FILE HANDLING FUNCTIONS
# --------------------------------------------------------------------------
def ensure_data_files():
    """Create the data directory and empty JSON data files if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for file_path, default in [
        (BOOKS_FILE, []),
        (MEMBERS_FILE, []),
        (TRANSACTIONS_FILE, []),
    ]:
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w") as f:
                    json.dump(default, f, indent=4)
            except OSError as e:
                print(f"[File Error] Could not create {file_path}: {e}")


def load_data(file_path):
    """Load JSON data from a file, return [] on any error."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[File Error] {file_path} not found. Starting with empty data.")
        return []
    except json.JSONDecodeError:
        print(f"[File Error] {file_path} is corrupted. Starting with empty data.")
        return []
    except OSError as e:
        print(f"[File Error] Problem reading {file_path}: {e}")
        return []


def save_data(file_path, data):
    """Save JSON data to a file with error handling."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError as e:
        print(f"[File Error] Could not save to {file_path}: {e}")
        return False


def get_valid_input(prompt, input_type=str, allow_empty=False):
    """Repeatedly prompt until a valid, non-empty value of the right type is given."""
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("[Input Error] This field cannot be empty. Please try again.")
            continue
        if input_type == int:
            try:
                return int(value)
            except ValueError:
                print("[Input Error] Please enter a valid whole number.")
                continue
        return value


def get_valid_choice(prompt, valid_choices):
    """Prompt until the user enters one of the valid menu choices."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"[Input Error] Invalid choice. Please select one of {valid_choices}.")


# --------------------------------------------------------------------------
# BOOK MANAGEMENT
# --------------------------------------------------------------------------
class BookManager:
    def __init__(self):
        self.books = load_data(BOOKS_FILE)

    def save(self):
        save_data(BOOKS_FILE, self.books)

    def find_book(self, book_id):
        for book in self.books:
            if book["book_id"] == book_id:
                return book
        return None

    def add_book(self):
        print("\n--- Add New Book ---")
        book_id = get_valid_input("Enter Book ID: ")

        if self.find_book(book_id):
            print(f"[Error] Book ID '{book_id}' already exists. Duplicate IDs are not allowed.")
            return

        title = get_valid_input("Enter Title: ")
        author = get_valid_input("Enter Author: ")
        category = get_valid_input("Enter Category/Genre: ")
        copies = get_valid_input("Enter Total Copies: ", int)

        if copies <= 0:
            print("[Error] Total copies must be a positive number.")
            return

        book = {
            "book_id": book_id,
            "title": title,
            "author": author,
            "category": category,
            "total_copies": copies,
            "available_copies": copies,
        }
        self.books.append(book)
        self.save()
        print(f"[Success] Book '{title}' added successfully.")

    def view_books(self):
        print("\n--- All Books ---")
        if not self.books:
            print("No books found in the library.")
            return
        header = f"{'ID':<10}{'Title':<25}{'Author':<20}{'Category':<15}{'Total':<8}{'Available':<10}"
        print(header)
        print("-" * len(header))
        for b in self.books:
            print(f"{b['book_id']:<10}{b['title']:<25}{b['author']:<20}"
                  f"{b['category']:<15}{b['total_copies']:<8}{b['available_copies']:<10}")

    def search_book(self):
        print("\n--- Search Book ---")
        keyword = get_valid_input("Enter Book ID, Title, or Author to search: ").lower()
        results = [
            b for b in self.books
            if keyword in b["book_id"].lower()
            or keyword in b["title"].lower()
            or keyword in b["author"].lower()
        ]
        if not results:
            print(f"[Info] No books found matching '{keyword}'.")
            return
        for b in results:
            print(f"\nID: {b['book_id']} | Title: {b['title']} | Author: {b['author']} | "
                  f"Category: {b['category']} | Available: {b['available_copies']}/{b['total_copies']}")


# --------------------------------------------------------------------------
# MEMBER MANAGEMENT
# --------------------------------------------------------------------------
class MemberManager:
    def __init__(self):
        self.members = load_data(MEMBERS_FILE)

    def save(self):
        save_data(MEMBERS_FILE, self.members)

    def find_member(self, member_id):
        for m in self.members:
            if m["member_id"] == member_id:
                return m
        return None

    def register_member(self):
        print("\n--- Register New Member ---")
        member_id = get_valid_input("Enter Member ID: ")

        if self.find_member(member_id):
            print(f"[Error] Member ID '{member_id}' already exists. Duplicate IDs are not allowed.")
            return

        name = get_valid_input("Enter Name: ")
        contact = get_valid_input("Enter Contact Number: ")
        email = get_valid_input("Enter Email: ")

        member = {
            "member_id": member_id,
            "name": name,
            "contact": contact,
            "email": email,
            "join_date": date.today().strftime(DATE_FORMAT),
            "status": "Active",
        }
        self.members.append(member)
        self.save()
        print(f"[Success] Member '{name}' registered successfully.")

    def view_members(self):
        print("\n--- All Members ---")
        if not self.members:
            print("No members found.")
            return
        header = f"{'ID':<10}{'Name':<20}{'Contact':<15}{'Email':<25}{'Joined':<12}{'Status':<10}"
        print(header)
        print("-" * len(header))
        for m in self.members:
            print(f"{m['member_id']:<10}{m['name']:<20}{m['contact']:<15}"
                  f"{m['email']:<25}{m['join_date']:<12}{m['status']:<10}")


# --------------------------------------------------------------------------
# TRANSACTION MANAGEMENT (ISSUE / RETURN / HISTORY)
# --------------------------------------------------------------------------
class TransactionManager:
    def __init__(self, book_manager, member_manager):
        self.transactions = load_data(TRANSACTIONS_FILE)
        self.book_manager = book_manager
        self.member_manager = member_manager

    def save(self):
        save_data(TRANSACTIONS_FILE, self.transactions)

    def _next_transaction_id(self):
        if not self.transactions:
            return "T001"
        last_num = max(int(t["transaction_id"][1:]) for t in self.transactions)
        return f"T{last_num + 1:03d}"

    def issue_book(self):
        print("\n--- Issue Book ---")
        book_id = get_valid_input("Enter Book ID: ")
        member_id = get_valid_input("Enter Member ID: ")

        book = self.book_manager.find_book(book_id)
        if not book:
            print(f"[Error] Book ID '{book_id}' not found.")
            return

        member = self.member_manager.find_member(member_id)
        if not member:
            print(f"[Error] Member ID '{member_id}' not found.")
            return

        if book["available_copies"] <= 0:
            print(f"[Error] Insufficient stock. '{book['title']}' is currently unavailable.")
            return

        transaction = {
            "transaction_id": self._next_transaction_id(),
            "book_id": book_id,
            "book_title": book["title"],
            "member_id": member_id,
            "member_name": member["name"],
            "issue_date": date.today().strftime(DATE_FORMAT),
            "return_date": None,
            "status": "Issued",
        }
        self.transactions.append(transaction)
        book["available_copies"] -= 1

        self.book_manager.save()
        self.save()
        print(f"[Success] Book '{book['title']}' issued to {member['name']} "
              f"(Transaction ID: {transaction['transaction_id']}).")

    def return_book(self):
        print("\n--- Return Book ---")
        transaction_id = get_valid_input("Enter Transaction ID: ")

        transaction = next(
            (t for t in self.transactions if t["transaction_id"] == transaction_id), None
        )
        if not transaction:
            print(f"[Error] Transaction ID '{transaction_id}' not found.")
            return

        if transaction["status"] == "Returned":
            print("[Error] This book has already been returned.")
            return

        transaction["return_date"] = date.today().strftime(DATE_FORMAT)
        transaction["status"] = "Returned"

        book = self.book_manager.find_book(transaction["book_id"])
        if book:
            book["available_copies"] += 1
            self.book_manager.save()

        self.save()
        print(f"[Success] Book '{transaction['book_title']}' returned successfully.")

    def borrowing_history(self):
        print("\n--- Borrowing History ---")
        member_id = get_valid_input("Enter Member ID (leave blank to view all): ", allow_empty=True)

        records = self.transactions
        if member_id:
            if not self.member_manager.find_member(member_id):
                print(f"[Error] Member ID '{member_id}' not found.")
                return
            records = [t for t in self.transactions if t["member_id"] == member_id]

        if not records:
            print("No borrowing history found.")
            return

        header = f"{'Txn ID':<8}{'Book':<20}{'Member':<15}{'Issued':<12}{'Returned':<12}{'Status':<10}"
        print(header)
        print("-" * len(header))
        for t in records:
            print(f"{t['transaction_id']:<8}{t['book_title']:<20}{t['member_name']:<15}"
                  f"{t['issue_date']:<12}{(t['return_date'] or '-'):<12}{t['status']:<10}")


# --------------------------------------------------------------------------
# REPORTS
# --------------------------------------------------------------------------
class ReportManager:
    def __init__(self, book_manager, member_manager, transaction_manager):
        self.book_manager = book_manager
        self.member_manager = member_manager
        self.transaction_manager = transaction_manager

    def book_report(self):
        books = self.book_manager.books
        total_books = sum(b["total_copies"] for b in books)
        available_books = sum(b["available_copies"] for b in books)
        borrowed_books = total_books - available_books

        print("\n--- Book Report ---")
        print(f"Total Books      : {total_books}")
        print(f"Available Books  : {available_books}")
        print(f"Borrowed Books   : {borrowed_books}")

    def member_report(self):
        members = self.member_manager.members
        total_members = len(members)
        active_members = sum(1 for m in members if m.get("status") == "Active")

        print("\n--- Member Report ---")
        print(f"Total Registered Members : {total_members}")
        print(f"Active Members           : {active_members}")

    def transaction_report(self):
        transactions = self.transaction_manager.transactions
        issued = len(transactions)
        returned = sum(1 for t in transactions if t["status"] == "Returned")
        pending = issued - returned

        print("\n--- Transaction Report ---")
        print(f"Total Books Issued  : {issued}")
        print(f"Total Books Returned: {returned}")
        print(f"Pending Returns     : {pending}")

    def generate_reports(self):
        print("\n===== LIBRARY REPORTS =====")
        self.book_report()
        self.member_report()
        self.transaction_report()

        export = get_valid_choice(
            "\nExport summary report to CSV? (y/n): ", ["y", "n", "Y", "N"]
        ).lower()
        if export == "y":
            self._export_csv()

    def _export_csv(self):
        report_path = os.path.join(DATA_DIR, "summary_report.csv")
        try:
            with open(report_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Report Generated On", date.today().strftime(DATE_FORMAT)])
                writer.writerow([])
                books = self.book_manager.books
                total_books = sum(b["total_copies"] for b in books)
                available_books = sum(b["available_copies"] for b in books)
                writer.writerow(["Book Report"])
                writer.writerow(["Total Books", total_books])
                writer.writerow(["Available Books", available_books])
                writer.writerow(["Borrowed Books", total_books - available_books])
                writer.writerow([])

                members = self.member_manager.members
                writer.writerow(["Member Report"])
                writer.writerow(["Total Registered Members", len(members)])
                writer.writerow(["Active Members",
                                  sum(1 for m in members if m.get("status") == "Active")])
                writer.writerow([])

                transactions = self.transaction_manager.transactions
                returned = sum(1 for t in transactions if t["status"] == "Returned")
                writer.writerow(["Transaction Report"])
                writer.writerow(["Total Books Issued", len(transactions)])
                writer.writerow(["Total Books Returned", returned])
                writer.writerow(["Pending Returns", len(transactions) - returned])
            print(f"[Success] Report exported to {report_path}")
        except OSError as e:
            print(f"[File Error] Could not export report: {e}")


# --------------------------------------------------------------------------
# MAIN MENU / APPLICATION LOOP
# --------------------------------------------------------------------------
def print_menu():
    print("\n==================================")
    print("   LIBRARY MANAGEMENT SYSTEM")
    print("==================================")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Register Member")
    print("5. View Members")
    print("6. Issue Book")
    print("7. Return Book")
    print("8. Borrowing History")
    print("9. Generate Reports")
    print("10. Exit")
    print("==================================")


def main():
    ensure_data_files()

    book_manager = BookManager()
    member_manager = MemberManager()
    transaction_manager = TransactionManager(book_manager, member_manager)
    report_manager = ReportManager(book_manager, member_manager, transaction_manager)

    actions = {
        "1": book_manager.add_book,
        "2": book_manager.view_books,
        "3": book_manager.search_book,
        "4": member_manager.register_member,
        "5": member_manager.view_members,
        "6": transaction_manager.issue_book,
        "7": transaction_manager.return_book,
        "8": transaction_manager.borrowing_history,
        "9": report_manager.generate_reports,
    }

    while True:
        print_menu()
        choice = get_valid_choice(
            "Enter your choice (1-10): ",
            [str(i) for i in range(1, 11)],
        )

        if choice == "10":
            print("\nThank you for using the Library Management System. Goodbye!")
            break

        try:
            actions[choice]()
        except Exception as e:
            # Catch-all safety net so the whole app never crashes unexpectedly
            print(f"[Unexpected Error] Something went wrong: {e}")


if __name__ == "__main__":
    main()
