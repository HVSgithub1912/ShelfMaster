import json
import random
import string
from pathlib import Path
from datetime import datetime


class Library:
    database = "library.json"

    data = {
        "books": [],
        "members": []
    }

    if Path(database).exists():
        with open(database, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4)

    @staticmethod
    def gen_id(prefix="B"):
        return prefix + "-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )

    def add_book(self, title, author, copies):
        book = {
            "id": Library.gen_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        Library.data["books"].append(book)
        Library.save_data()

    def add_member(self, name, email):

        member = {
            "id": Library.gen_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }

        Library.data["members"].append(member)
        Library.save_data()

    def borrow_book(self, book_id, member_id):

        books = [
            b for b in Library.data["books"]
            if b["id"] == book_id
        ]

        if not books:
            return "Book not found"

        book = books[0]

        members = [
            m for m in Library.data["members"]
            if m["id"] == member_id
        ]

        if not members:
            return "Member not found"

        member = members[0]

        if book["available_copies"] <= 0:
            return "No copies available"

        borrow_entry = {
            "book_id": book_id,
            "book_name": book["title"],
            "borrow_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        member["borrowed"].append(borrow_entry)

        book["available_copies"] -= 1

        Library.save_data()

        return "Book borrowed successfully"

    def return_book(self, member_id, book_id):

        members = [
            m for m in Library.data["members"]
            if m["id"] == member_id
        ]

        if not members:
            return "Member not found"

        member = members[0]

        for b in member["borrowed"]:

            if b["book_id"] == book_id:

                member["borrowed"].remove(b)

                books = [
                    bk for bk in Library.data["books"]
                    if bk["id"] == book_id
                ]

                if books:
                    books[0]["available_copies"] += 1

                Library.save_data()

                return "Book returned successfully"

        return "Book not borrowed"