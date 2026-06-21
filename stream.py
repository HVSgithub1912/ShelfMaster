import streamlit as st
import pandas as pd
from library import Library

lib = Library()

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Library Management System")

menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Add Book",
        "View Books",
        "Add Member",
        "View Members",
        "Borrow Book",
        "Return Book"
    ]
)

# ------------------------------------------------
# ADD BOOK
# ------------------------------------------------

if menu == "Add Book":

    st.subheader("Add New Book")

    title = st.text_input("Book Title")

    author = st.text_input("Author")

    copies = st.number_input(
        "Number of Copies",
        min_value=1,
        step=1
    )

    if st.button("Add Book"):

        lib.add_book(title, author, copies)

        st.success("Book Added Successfully")


# ------------------------------------------------
# VIEW BOOKS
# ------------------------------------------------

elif menu == "View Books":

    st.subheader("Available Books")

    if Library.data["books"]:

        df = pd.DataFrame(
            Library.data["books"]
        )

        st.dataframe(df)

    else:
        st.warning("No books available")


# ------------------------------------------------
# ADD MEMBER
# ------------------------------------------------

elif menu == "Add Member":

    st.subheader("Add Member")

    name = st.text_input("Member Name")

    email = st.text_input("Email")

    if st.button("Add Member"):

        lib.add_member(name, email)

        st.success("Member Added Successfully")


# ------------------------------------------------
# VIEW MEMBERS
# ------------------------------------------------

elif menu == "View Members":

    st.subheader("Members")

    if Library.data["members"]:

        members = []

        for m in Library.data["members"]:

            members.append({
                "ID": m["id"],
                "Name": m["name"],
                "Email": m["email"],
                "Borrowed Books": len(m["borrowed"])
            })

        st.dataframe(pd.DataFrame(members))

    else:
        st.warning("No members available")


# ------------------------------------------------
# BORROW BOOK
# ------------------------------------------------

elif menu == "Borrow Book":

    st.subheader("Borrow Book")

    book_options = {
        f"{b['title']} ({b['id']})": b["id"]
        for b in Library.data["books"]
    }

    member_options = {
        f"{m['name']} ({m['id']})": m["id"]
        for m in Library.data["members"]
    }

    if book_options and member_options:

        selected_book = st.selectbox(
            "Select Book",
            list(book_options.keys())
        )

        selected_member = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        if st.button("Borrow"):

            msg = lib.borrow_book(
                book_options[selected_book],
                member_options[selected_member]
            )

            st.success(msg)

    else:
        st.warning("Books or Members not available")


# ------------------------------------------------
# RETURN BOOK
# ------------------------------------------------

elif menu == "Return Book":

    st.subheader("Return Book")

    member_options = {
        f"{m['name']} ({m['id']})": m["id"]
        for m in Library.data["members"]
    }

    if member_options:

        selected_member = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        member_id = member_options[selected_member]

        member = next(
            m for m in Library.data["members"]
            if m["id"] == member_id
        )

        borrowed = member["borrowed"]

        if borrowed:

            book_options = {
                f"{b['book_name']} ({b['book_id']})":
                b["book_id"]
                for b in borrowed
            }

            selected_book = st.selectbox(
                "Borrowed Books",
                list(book_options.keys())
            )

            if st.button("Return Book"):

                msg = lib.return_book(
                    member_id,
                    book_options[selected_book]
                )

                st.success(msg)

        else:
            st.info("No borrowed books")

    else:
        st.warning("No members found")