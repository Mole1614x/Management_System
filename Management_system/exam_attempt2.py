import sqlite3
import csv
import json
from datetime import datetime

#-------------------------------- DATABASE ---------------------------------#

conn = sqlite3.connect("bank.db", isolation_level=None)
cursor = conn.cursor()

#----------------------- Create Table -------------------------------------#
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    account_type TEXT,
    balance REAL,
    created_date TEXT
)
""")

#------------------------------- clear table ------------------------------#
cursor.execute("DELETE FROM accounts")

#------------------------------- Reset autoincrement -----------------------#
cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts'")

#----------------------------- data -----------------------------------------#
data = [
    ("Ravi Kumar","Savings",15000,"2026-04-01"),
    ("Anjali Sharma","Current",50000,"2026-04-02"),
    ("Sudesh Reddy","Savings",22000,"2026-04-03"),
    ("Meena Iyer","Current",75000,"2026-04-04"),
    ("Arjun Das","Savings",12000,"2026-04-05")
]

#----------------------------- Insert Values --------------------------------#
cursor.executemany(
    "INSERT INTO accounts(customer_name,account_type,balance,created_date) VALUES(?,?,?,?)",
    data
)
print("Records updated Successfully!")


#--------------------------------- OOP LAYER --------------------------------#
class BankAccount:

    def __init__(self,customer_name,account_type,balance,created_date):
        self.customer_name =customer_name
        self.account_type = account_type
        self.balance = balance
        self.created_date = created_date

    def __str__(self):
        return f"|Name: {self.customer_name}| Account Type: {self.account_type}| Balance: {self.balance}| Created_date: {self.created_date}"

    def to_dict(self):
        return {
            "customer_name": self.customer_name,
            "account_type" : self.account_type,
            "balance" : self.balance,
            "created_date" : self.created_date
        }
    
    @staticmethod
    def from_dict(data):
        return BankAccount(
            data["customer_name"],
            data["account_type"],
            data["balance"],
            data["created_date"]
        )
    
    #------------------------------ Validations -------------------------------#

    @staticmethod
    def validate_name(name):
        return name.strip() != ""

    @staticmethod
    def validate_type(acc_type):
        return acc_type in ['Savings','Current']

    @staticmethod
    def validate_balance(bal):
        return bal >= 0

    @staticmethod
    def validate_transaction_amount(amount):
        return amount > 0

    @staticmethod
    def validate_withdrawl(amount,bal):
        return 0 <= amount <= bal

    @staticmethod
    def validate_date(c_date):
        try:
            datetime.strptime(c_date, "%Y-%m-%d")
            return True
        except:
            return False

    #=============================== CRUD ===========================#

    def add_values(self):
        name = input("Enter your name:")
        if not BankAccount.validate_name(name):
            print("Invalid name!")
            return

        acc_type = input("Enter account type (Savings/Current): ")
        if not BankAccount.validate_type(acc_type):
            print("Invalid Type!")
            return

        bal = float(input("Enter your balance:"))
        if not BankAccount.validate_balance(bal):
            print("Invalid Balance!")
            return
        
        c_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO accounts(customer_name,account_type,balance,created_date) VALUES(?,?,?,?)",
            (name,acc_type,bal,c_date)
        )

    def view(self):
        cursor.execute("SELECT * FROM accounts")
        print("Records:")
        for row in cursor.fetchall():
            print(row)

    def delete_values(self):
        del_id = int(input("Enter ID:"))
        cursor.execute("DELETE FROM accounts WHERE account_id = ?",(del_id,))
        print("Deleted!")

    def search_value(self):
        print("1.By ID\n2.By Name\n3.By Type")
        ch = int(input("Enter choice:"))

        if ch == 1:
            s_id = int(input("Enter ID:"))
            cursor.execute("SELECT * FROM accounts WHERE account_id = ?",(s_id,))
        elif ch == 2:
            s_name = input("Enter name:")
            cursor.execute("SELECT * FROM accounts WHERE customer_name LIKE ?",('%'+s_name+'%',))
        elif ch == 3:
            s_type = input("Enter type:")
            cursor.execute("SELECT * FROM accounts WHERE account_type = ?",(s_type,))
        else:
            print("Invalid choice!")
            return

        print(cursor.fetchall())

    def update_value(self):
        name = input("Enter name:")
        a_type = input("Enter new type:")
        cursor.execute("UPDATE accounts SET account_type = ? WHERE customer_name = ?",(a_type,name))
        print("Updated!")

    #================ Transactions =================#

    def Deposit_money(self):
        acc_id = int(input("Enter ID: "))
        amt = float(input("Enter amount: "))
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?",(amt,acc_id))
        print("Deposited!")

    def withdraw_money(self):
        acc_id = int(input("Enter ID: "))
        amt = float(input("Enter amount: "))

        cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (acc_id,))
        res = cursor.fetchone()

        if res and res[0] >= amt:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amt, acc_id))
            print("Withdraw Successful!")
        else:
            print("Insufficient Balance!")

    #================ Export / Import =================#

    def export_csv(self):
        cursor.execute("SELECT * FROM accounts")
        records = cursor.fetchall()

        with open("accounts.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["account_id","customer_name","account_type","balance","created_date"])
            writer.writerows(records)

        print("CSV Exported!")

    def import_csv(self):
        with open("accounts.csv","r") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                cursor.execute(
                    "INSERT OR IGNORE INTO accounts(account_id,customer_name,account_type,balance,created_date) VALUES(?,?,?,?,?)",
                    (int(row[0]),row[1],row[2],float(row[3]),row[4])
                )

        print("CSV Imported!")

    def export_json(self):
        cursor.execute("SELECT * FROM accounts")
        records = cursor.fetchall()

        data = []
        for row in records:
            data.append({
                "account_id":row[0],
                "customer_name":row[1],
                "account_type":row[2],
                "balance":row[3],
                "created_date":row[4]
            })

        with open("accounts.json","w") as f:
            json.dump(data,f,indent=4)

        print("JSON Exported!")

    def import_json(self):
        with open("accounts.json","r") as f:
            data = json.load(f)

        for item in data:
            cursor.execute(
                "INSERT OR IGNORE INTO accounts(account_id,customer_name,account_type,balance,created_date) VALUES(?,?,?,?,?)",
                (item["account_id"],item["customer_name"],item["account_type"],item["balance"],item["created_date"])
            )

        print("JSON Imported!")


#=============================== MENU ==============================#

obj = BankAccount()

while True:
    try:
        print("""
                1.Create
                2.View
                3.Delete
                4.Search
                5.Update
                6.Deposit
                7.Withdraw
                8.Export CSV
                9.Export JSON
                10.Import CSV
                11.Import JSON
                12.Exit
                """)

        ch = int(input("Enter choice:"))

        if ch == 1: obj.add_values()
        elif ch == 2: obj.view()
        elif ch == 3: obj.delete_values()
        elif ch == 4: obj.search_value()
        elif ch == 5: obj.update_value()
        elif ch == 6: obj.Deposit_money()
        elif ch == 7: obj.withdraw_money()
        elif ch == 8: obj.export_csv()
        elif ch == 9: obj.export_json()
        elif ch == 10: obj.import_csv()
        elif ch == 11: obj.import_json()
        elif ch == 12:
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

    except Exception as e:
        print("ERROR:", e)