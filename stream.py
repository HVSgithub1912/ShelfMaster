import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from library import Library

lib = Library()

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.card {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

.metric {
    font-size: 35px;
    font-weight: bold;
    color: #60A5FA;
}

.label {
    font-size: 18px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    selected = option_menu(
        "Library Portal",
        [
            "Dashboard",
            "Books",
            "Members",
            "Borrow",
            "Return"
        ],
        icons=[
            "house",
            "book",
            "people",
            "arrow-right-circle",
            "arrow-left-circle"
        ],
        default_index=0
    )

# -------------------------
# DATA
# -------------------------

books = Library.data["books"]
members = Library.data["members"]

total_books = len(books)

available_books = sum(
    b["available_copies"]
    for b in books
)

borrowed_books = sum(
    b["total_copies"] - b["available_copies"]
    for b in books
)

total_members = len(members)

# -------------------------
# DASHBOARD
# -------------------------

if selected == "Dashboard":

    st.title("📚 Library Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card">
        <div class="metric">{total_books}</div>
        <div class="label">Books</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
        <div class="metric">{available_books}</div>
        <div class="label">Available</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
        <div class="metric">{borrowed_books}</div>
        <div class="label">Borrowed</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="card">
        <div class="metric">{total_members}</div>
        <div class="label">Members</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    left, right = st.columns(2)

    with left:

        fig = px.pie(
            names=["Available", "Borrowed"],
            values=[available_books, borrowed_books],
            title="Book Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        if books:

            df = pd.DataFrame(books)

            author_counts = (
                df.groupby("author")
                .size()
                .reset_index(name="books")
            )

            fig2 = px.bar(
                author_counts,
                x="author",
                y="books",
                title="Books by Author"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    st.subheader("Recent Books")

    if books:
        st.dataframe(
            pd.DataFrame(books),
            use_container_width=True
        )

# -------------------------
# BOOKS
# -------------------------

elif selected == "Books":

    tab1, tab2 = st.tabs(
        ["Add Book", "View Books"]
    )

    with tab1:

        st.subheader("Add New Book")

        title = st.text_input("Book Title")

        author = st.text_input("Author")

        copies = st.number_input(
            "Copies",
            min_value=1,
            step=1
        )

        if st.button("Add Book"):

            lib.add_book(
                title,
                author,
                copies
            )

            st.success("Book Added")

    with tab2:

        if books:

            search = st.text_input(
                "🔍 Search Book"
            )

            filtered = [
                b for b in books
                if search.lower()
                in b["title"].lower()
            ]

            st.dataframe(
                pd.DataFrame(filtered),
                use_container_width=True
            )

# -------------------------
# MEMBERS
# -------------------------

elif selected == "Members":

    tab1, tab2 = st.tabs(
        ["Add Member", "View Members"]
    )

    with tab1:

        name = st.text_input("Name")

        email = st.text_input("Email")

        if st.button("Register Member"):

            lib.add_member(
                name,
                email
            )

            st.success("Member Registered")

    with tab2:

        member_data = []

        for m in members:

            member_data.append({
                "ID": m["id"],
                "Name": m["name"],
                "Email": m["email"],
                "Borrowed": len(
                    m["borrowed"]
                )
            })

        st.dataframe(
            pd.DataFrame(member_data),
            use_container_width=True
        )

# -------------------------
# BORROW
# -------------------------

elif selected == "Borrow":

    st.subheader("Borrow Book")

    if books and members:

        book_map = {
            f"{b['title']} ({b['id']})":
            b["id"]
            for b in books
        }

        member_map = {
            f"{m['name']} ({m['id']})":
            m["id"]
            for m in members
        }

        book = st.selectbox(
            "Select Book",
            list(book_map.keys())
        )

        member = st.selectbox(
            "Select Member",
            list(member_map.keys())
        )

        if st.button("Borrow"):

            msg = lib.borrow_book(
                book_map[book],
                member_map[member]
            )

            st.success(msg)

# -------------------------
# RETURN
# -------------------------

elif selected == "Return":

    st.subheader("Return Book")

    if members:

        member_map = {
            f"{m['name']} ({m['id']})":
            m["id"]
            for m in members
        }

        selected = st.selectbox(
            "Member",
            list(member_map.keys())
        )

        member_id = member_map[selected]

        member = next(
            m for m in members
            if m["id"] == member_id
        )

        borrowed = member["borrowed"]

        if borrowed:

            book_map = {
                f"{b['book_name']}":
                b["book_id"]
                for b in borrowed
            }

            selected_book = st.selectbox(
                "Book",
                list(book_map.keys())
            )

            if st.button("Return"):

                msg = lib.return_book(
                    member_id,
                    book_map[selected_book]
                )

                st.success(msg)