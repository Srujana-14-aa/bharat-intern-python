
import streamlit as st
import json
import os

st.set_page_config(page_title="Library Management System", page_icon="📚")

st.title("📚 Library Management System")
st.write("Manage books, members, issuing and returning books.")

# JSON file handling
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

books = load_data("books.json")
members = load_data("members.json")
transactions = load_data("transactions.json")

menu = st.sidebar.selectbox(
    "Select Menu",
    ["Home", "Add Book", "View Books",
     "Add Member", "View Members",
     "Issue Book", "Return Book", "Transactions"]
)

if menu == "Home":
    st.subheader("Welcome!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Books", len(books))
    col2.metric("Total Members", len(members))
    col3.metric("Transactions", len(transactions))

elif menu == "Add Book":
    st.subheader("Add New Book")
    book_id = st.text_input("Book ID")
    title = st.text_input("Book Title")
    author = st.text_input("Author")

    if st.button("Add Book"):
        if not book_id or not title or not author:
            st.warning("Please fill all fields.")
        elif any(b["id"] == book_id for b in books):
            st.error("Book ID already exists.")
        else:
            books.append({
                "id": book_id,
                "title": title,
                "author": author,
                "available": True
            })
            save_data("books.json", books)
            st.success("Book added successfully!")

elif menu == "View Books":
    st.subheader("Available Books")
    if books:
        st.dataframe(books, use_container_width=True)
    else:
        st.info("No books available.")

elif menu == "Add Member":
    st.subheader("Register Member")
    member_id = st.text_input("Member ID")
    name = st.text_input("Member Name")

    if st.button("Register Member"):
        if not member_id or not name:
            st.warning("Please fill all fields.")
        elif any(m["id"] == member_id for m in members):
            st.error("Member ID already exists.")
        else:
            members.append({"id": member_id, "name": name})
            save_data("members.json", members)
            st.success("Member registered successfully!")

elif menu == "View Members":
    st.subheader("Registered Members")
    if members:
        st.dataframe(members, use_container_width=True)
    else:
        st.info("No members registered.")

elif menu == "Issue Book":
    st.subheader("Issue a Book")

    available_books = [b for b in books if b["available"]]

    if available_books and members:
        selected_book = st.selectbox(
            "Select Book",
            available_books,
            format_func=lambda b: f'{b["id"]} - {b["title"]}'
        )
        selected_member = st.selectbox(
            "Select Member",
            members,
            format_func=lambda m: f'{m["id"]} - {m["name"]}'
        )

        if st.button("Issue Book"):
            selected_book["available"] = False
            transactions.append({
                "book_id": selected_book["id"],
                "member_id": selected_member["id"],
                "status": "Issued"
            })
            save_data("books.json", books)
            save_data("transactions.json", transactions)
            st.success("Book issued successfully!")
    else:
        st.info("Add an available book and a member first.")

elif menu == "Return Book":
    st.subheader("Return a Book")

    issued = [
        t for t in transactions
        if t["status"] == "Issued"
    ]

    if issued:
        selected = st.selectbox(
            "Select issued book",
            issued,
            format_func=lambda t: t["book_id"]
        )

        if st.button("Return Book"):
            for book in books:
                if book["id"] == selected["book_id"]:
                    book["available"] = True
                    break

            selected["status"] = "Returned"

            save_data("books.json", books)
            save_data("transactions.json", transactions)
            st.success("Book returned successfully!")
    else:
        st.info("No books are currently issued.")

elif menu == "Transactions":
    st.subheader("Transaction History")
    if transactions:
        st.dataframe(transactions, use_container_width=True)
    else:
        st.info("No transactions yet.")
