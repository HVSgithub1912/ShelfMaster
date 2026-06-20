import json
import random 
import string
from pathlib import Path
from datetime import datetime

class Library:
    database = "library.json"
    data = {
        "books": [], "members": []
    }
    #load existing data to json or create your json
    if Path(database).exists():
        with open(database, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    # else: 
    #     with open(database , "w") as f:
    #         json.dump(data , f ,indent=2)

    @classmethod
    def save_data(cls):# because i don't want anyone do perform this operation outside the class , and class method are only accesed inside the class
        with open (cls.database, 'w') as f:
            json.dump(cls.data, f, indent=4, default=str)


    def gen_id(Prefix = "B"):
        book_id = ""
        for i in range(5):
            book_id += random.choice(string.ascii_uppercase + string.digits)

        return Prefix + "-" + book_id
    
    def add_book(self):
        title = input("Enter Book title: ")
        author = input("give name of the author: ")
        copies = int(input("how many copies do you have? "))
        book = {
            "id": Library.gen_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")        


        }
        Library.data['books'].append(book)
        Library.save_data()

    def list_books(self):
        if not Library.data["books"]:
            print("No book is available right now ")
            return 
        for b in Library.data["books"]:
            print(f"{b['id']:12}{b['title'][:20]:12} {b['author'][:24]}")

    def add_member(self):
        name = input("enter name of your member: ")
        email = input("enter the mail: ")
        member = {
            "id": Library.gen_id("M"),
            "name": name,
            "email" : email,
            "borrowed" : []

        }
        Library.data['members'].append(member)
        Library.save_data()
        print(member)
        print("New member added successfully ")

    def list_members(self):
        if not Library.data['members']:
            print("No member right now ")
            return
        for m in Library.data['members']:
            print(f"{m['id']:12} {m['name']:12} {m['email']:12}")
            print(f"Books borrowed are {m['borrowed']}")

    


obj = Library()

print("="*50)
print("LIBRARY MANAGEMENT SYSTEM")
print("="*50)
print("1. Add Book")
print("2. List Books")
print("3. Add members")
print("4. list members")
print("5. Borrow book")
print("0. Exit portal")
print("-"*50)
choice = int(input("What task you want to do? "))
if choice == 1:
    obj.add_book()
elif choice == 2:
    obj.list_books()
elif choice == 3:
    obj.add_member()
elif choice == 4:
    obj.list_members()
elif choice == 5:
    obj.borrow_book()
elif choice == 0:
    obj.exit_portal()