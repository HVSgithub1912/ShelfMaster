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
    else: 
        with open(database , "w") as f:
            json.dump(data , f ,indent=2)

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
    