#----------------------------- Imports --------------------------------#
import sqlite3
import csv 
import json
from datetime import date

#------------------------------- Database ------------------------------#
conn = sqlite3.connect("train.db",isolation_level=None)
cursor = conn.cursor()

#-------------------------------- Table Creation -----------------------#
cursor.execute("create table if not exists users(user_id integer primary key autoincrement, username text, password text)")

cursor.execute("create table if not exists trains(train_id integer primary key autoincrement, train_name text, source text, destination text, total_seats integer, available_seats integer)")

cursor.execute("create table if not exists reservations(reservation_id integer primary key autoincrement,user_id integer, train_id integer, passenger_name text, seats_booked integer, status text, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(train_id) REFERENCES trains(train_id))")

#-------------------- Reset (Testing) ----------------#
cursor.execute("delete from users")
cursor.execute("delete from trains")
cursor.execute("delete from reservations")
cursor.execute("delete from sqlite_sequence where name = 'users'")
cursor.execute("delete from sqlite_sequence where name = 'trains'")
cursor.execute("delete from sqlite_sequence where name = 'reservations'")


#------------------------- Class Structure --------------------------------#

class ReservationSystem:

    @staticmethod
    def add_trains():
        t_name = input("Enter Train Name: ").strip()
        source = input("Enter Source: ").strip()
        destination = input("Enter Destination: ").strip()
        total_seats = 25
        available_seats = total_seats

        cursor.execute(
            "insert into trains(train_name, source, destination, total_seats, available_seats) values(?,?,?,?,?)",
            (t_name, source, destination, total_seats, available_seats)
        )
        print("Train Added Successfully!")

    @staticmethod
    def view_trains():
        cursor.execute("select * from trains")
        for row in cursor.fetchall():
            print(row)

    @staticmethod
    def book_ticket():
        train_id = int(input("Enter train id: "))
        name = input("Enter passenger name: ")
        seats = int(input("Enter seats: "))

        cursor.execute("select available_seats from trains where train_id=?", (train_id,))
        result = cursor.fetchone()

        if result and result[0] >= seats:
            cursor.execute(
                "insert into reservations(user_id,train_id,passenger_name,seats_booked,status) values(NULL,?,?,?,?)",
                (train_id, name, seats, "BOOKED")
            )

            cursor.execute(
                "update trains set available_seats = available_seats - ? where train_id=?",
                (seats, train_id)
            )

            print("Ticket Booked!")
        else:
            print("Not enough seats!")

    @staticmethod
    def cancel_ticket():
        rid = int(input("Enter reservation id: "))

        cursor.execute("select train_id, seats_booked from reservations where reservation_id=?", (rid,))
        result = cursor.fetchone()

        if result:
            train_id, seats = result

            cursor.execute("update reservations set status='CANCELLED' where reservation_id=?", (rid,))
            cursor.execute(
                "update trains set available_seats = available_seats + ? where train_id=?",
                (seats, train_id)
            )

            print("Ticket Cancelled!")

    @staticmethod
    def view_reservations():
        cursor.execute("select * from reservations")
        for row in cursor.fetchall():
            print(row)

    @staticmethod
    def export_csv():
        cursor.execute("select * from trains")
        rows = cursor.fetchall()

        with open("trains.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id","name","source","destination","total","available"])
            writer.writerows(rows)

        print("Exported to CSV!")

    @staticmethod
    def import_csv():
        with open("trains.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                cursor.execute(
                    "insert into trains(train_name, source, destination, total_seats, available_seats) values(?,?,?,?,?)",
                    (row[1], row[2], row[3], row[4], row[5])
                )

        print("Imported from CSV!")

    @staticmethod
    def export_json():
        cursor.execute("select * from trains")
        rows = cursor.fetchall()

        data = []
        for r in rows:
            data.append({
                "name": r[1],
                "source": r[2],
                "destination": r[3],
                "total": r[4]
            })

        with open("trains.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Exported to JSON!")

    @staticmethod
    def import_json():
        with open("trains.json", "r") as f:
            data = json.load(f)

        for d in data:
            cursor.execute(
                "insert into trains(train_name, source, destination, total_seats, available_seats) values(?,?,?,?,?)",
                (d["name"], d["source"], d["destination"], d["total"], d["total"])
            )

        print("Imported from JSON!")


#------------------------- MENU + MAIN -----------------------------#

def main():
    while True:
        print("\n------ TRAIN RESERVATION SYSTEM ------")
        print("1. Add Train")
        print("2. View Trains")
        print("3. Book Ticket")
        print("4. Cancel Ticket")
        print("5. View Reservations")
        print("6. Export CSV")
        print("7. Import CSV")
        print("8. Export JSON")
        print("9. Import JSON")
        print("10. Exit")

        ch = input("Enter choice: ")

        if ch == "1": ReservationSystem.add_trains()
        elif ch == "2": ReservationSystem.view_trains()
        elif ch == "3": ReservationSystem.book_ticket()
        elif ch == "4": ReservationSystem.cancel_ticket()
        elif ch == "5": ReservationSystem.view_reservations()
        elif ch == "6": ReservationSystem.export_csv()
        elif ch == "7": ReservationSystem.import_csv()
        elif ch == "8": ReservationSystem.export_json()
        elif ch == "9": ReservationSystem.import_json()
        elif ch == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()