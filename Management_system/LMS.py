import sqlite3
import csv
import json

# Database
conn = sqlite3.connect("lms.db", isolation_level=None)
cursor = conn.cursor()

# create command for table books and issued_books

cursor.execute("create table if not exists books(book_id integer primary key autoincrement, title text, author text, is_available integer)")

cursor.execute("create table if not exists issued_books(issued_id integer primary key autoincrement, book_id integer, user_name text, issue_date text, return_date text, FOREIGN KEY(book_id) REFERENCES books(book_id))")


# Testing purpose 

cursor.execute("delete from books")
cursor.execute("delete from sqlite_sequence where name = 'books'")
cursor.execute("delete from issued_books")
cursor.execute("delete from sqlite_sequence where name = 'issued_books'")

# data to insert
data = [
    ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1),
    ("The Monk Who Sold His Ferrari", "Robin Sharma", 1),
    ("Man's Search for Meaning", "Viktor E. Frankl", 1),
    ("The White Tiger", "Aravind Adiga", 1),
    ("Journey to the End of the Earth", "Tishani Doshi", 1),
    ("Rich Dad Poor Dad", "Robert T. Kiyosaki", 1),
    ("Solo Leveling Volume 1", "Mappa", 1)
]

# Insert data in books (FIXED QUERY)

cursor.executemany("insert into books(title,author,is_available) values(?,?,?)", data)
print("Records updated Successfully!")


# View
cursor.execute("select * from books")
record = cursor.fetchall()
for row in record:
    print(row)


class Book:

    def __init__(self,title,author,is_available):
        self.title = title
        self.author = author
        self.is_available = is_available

    def __str__(self):
        return f"|Title: {self.title}| Author: {self.author}| Availability: {self.is_available}"
    
class Library:

    @staticmethod
    def add_book():

        title = input("Enter the title:")
        author = input("Enter the author:")
        is_available = 1

        # FIXED COLUMN NAME
        cursor.execute("insert into books(title,author,is_available) values (?,?,?)",(title,author,is_available))

        print("Record updated Successfully!")

    @staticmethod
    def view_book():

        cursor.execute("select * from books")
        record = cursor.fetchall()
        for row in record:
            print(row)

    @staticmethod
    def issue_book():

        book_id = int(input("Enter the book_id:"))
        user_name = input("Enter the username:")

        # FETCH RESULT
        cursor.execute("select is_available from books where book_id = ?",(book_id,))
        result = cursor.fetchone()

        if result is None:
            print("Book not found!")
            return

        if result[0] == 0:
            print("Book already issued!")
            return

        from datetime import datetime
        issue_date = str(datetime.now().date())
        return_date = "7 days later"

        cursor.execute("insert into issued_books(book_id,user_name,issue_date,return_date) values(?,?,?,?)",(book_id,user_name,issue_date,return_date))

        cursor.execute("update books set is_available = 0 where book_id = ?",(book_id,))

        print("Book issued successfully!")

    @staticmethod
    def return_book():

        book_id = int(input("Enter the book_id:"))

        # FIXED TUPLE
        cursor.execute("update issued_books set return_date = CURRENT_DATE where book_id = ? AND return_date is null", (book_id,))

        cursor.execute("update books set is_available = 1 where book_id = ?",(book_id,))

        print("Book returned successfully!")

    @staticmethod
    def view_available():
        
        cursor.execute("Select * from books where is_available = 1")
        avail = cursor.fetchall()
        print(f"The Available books are: {avail}")

    @staticmethod
    def view_issued():

        cursor.execute("select * from issued_books where return_date IS NULL")
        print(f" The issued Books are: {cursor.fetchall()}")

    @staticmethod
    def export_csv():
        try:
            cursor.execute("select * from books")
            rows = cursor.fetchall()

            with open("books.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["book_id","title","author","is_available"])
                writer.writerows(rows)
                print("Books exported to csv successfully!")
        except Exception as e:
            print("Error:",e)

    @staticmethod
    def import_csv():
        try:
            with open("books.csv", "r" ) as f:
                rows =csv.reader(f)
                next(rows) # skip header

                for row in rows:
                    cursor.execute("insert into books(title,author,is_available) values(?,?,?)",(row[1],row[2]),row[3])
            print("Books imported from CSV successfully!")
        
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def export_json():
        try:
            cursor.execute("select * from books")
            rows = cursor.fetchall()

            data =[]
            for row in rows:
                data.append({
                    "book_id":row[0],
                    "title": row[1],
                    "author": row[2],
                    "is_avaiable": row[3]
                })
            with open("books.json", "w") as f:
                json.dump(data,f, indent=4)

            print("Books exported to json successfully!")
        
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def import_json():
        try: 
            with open("books.json","r") as f:
                data = json.load(f)
            for item in data:
                cursor.execute(
                "INSERT INTO books(title, author, is_available) VALUES (?, ?, ?)",
                (item["title"], item["author"], item["is_available"])
            )
            
            print("Books imported Successfully!")

        except Exception as e:
            print("Error:",e)

def main():
    while True:

        print("------------- LIBRARY MENU ---------------")
        print("1. Add Books")
        print("2. View All Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Available Books")
        print("6. View Issued Books")
        print("7. Exit")

        ch = int(input("Enter your choice:"))

        if ch == 1: Library.add_book()
        elif ch == 2: Library.view_book()
        elif ch == 3: Library.issue_book()
        elif ch == 4: Library.return_book()
        elif ch == 5: Library.view_available()
        elif ch == 6: Library.view_issued()
        elif ch == 7: Library.export_csv()
        elif ch == 8: Library.export_json()
        elif ch == 9: Library.import_csv()
        elif ch == 10:Library.import_json() 
        elif ch == 11: 
            print("Thank you for Visiting....") 
            break
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()