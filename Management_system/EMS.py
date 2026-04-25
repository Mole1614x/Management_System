import sqlite3
import csv
import json

# Database

conn = sqlite3.connect("employee.db",isolation_level=None)
cursor = conn.cursor()

#Create table Employee

cursor.execute("create table if not exists employees(id integer primary key autoincrement, name text, salary real, department text)")


# Delete Testing pursposse and sqlite

cursor.execute("delete from employees") 
cursor.execute("delete from sqlite_sequence where name = 'employees' ")



# Class and object


class Employee:

    def __init__(self,name,salary,department):
        self.name = name
        self.salary = salary
        self.department = department

    def __str__(self):
        return f"|Name: {self.name}| Salary: {self.salary}| Department: {self.department}|"

class EmployeeManager:

    @staticmethod
    def add_employee():

        name = input("Enter your name:")
        salary = int(input("Enter your salary:"))
        department = input("Enter your department:")

        cursor.execute("insert into employees(name,salary,department) values(?,?,?)",(name,salary,department))

        print("Record Created Successfully!")

    @staticmethod
    def view_employees():

        cursor.execute("select * from employees")
        rows = cursor.fetchall()
        print("Employee Records")

        for row in rows:
            print(row)

    @staticmethod
    def update_salary():

        emp_id = int(input("Enter your Employee id:"))
        new_salary = int(input("Enter your new salary:"))

        cursor.execute("update employees set salary = ? where id = ?",(new_salary, emp_id))  # FIXED (order)
        print("Record Updated Successfully!")   

    @staticmethod
    def search_by_department():

        department = input("Enter your department for search:") 
        cursor.execute("select * from employees where department = ?",(department,))
        rows = cursor.fetchall()  # FIXED
        for row in rows:  # FIXED
            print(row)  # FIXED

    @staticmethod
    def delete_employee():

        emp_id = int(input("Enter your employee id to delete:"))

        cursor.execute("delete from employees where id =?",(emp_id,))
        print("Record Deleted Successfully!")

    @staticmethod
    def export_csv():
        try:
            cursor.execute("select * from employees")
            rows = cursor.fetchall()
            next(rows)

            with open("employees.csv","w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id","name","salary","department"])  # FIXED
                writer.writerows(rows)
                print("Records exported to csv successfully!")
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def import_csv():
        try:
            with open("employees.csv","r") as f:
                rows = csv.reader(f)

                for row in rows:
                    cursor.execute("insert into employees(name,salary,department) values(?,?,?)",(row[1],row[2],row[3]))  
            print("Records imported successfully!")
        except Exception as e:
            print("Error:",e)

    @staticmethod
    def export_json():
        
        try:
            cursor.execute("select * from employees")
            rows = cursor.fetchall()

            data = []
            for row in rows:
                data.append({
                    "name":row[1],
                    "salary": row[2],
                    "department":row[3]
                })

            with open("employees.json","w") as f:
                json.dump(data,f,indent=4)

            print("Records exported successfully!")

        except Exception as e:
            print("Error:",e)

    @staticmethod
    def import_json():

        try:
            with open("employees.json","r") as f:
                reader = json.load(f)

                for row in reader:
                    cursor.execute("insert into employees(name,salary,department) values(?,?,?)",(row["name"],row["salary"],row["department"]))

            print("Records imported successfully!")
        
        except Exception as e:
            print("Error:",e)


def main():

    while True:

        print("---------------------- Employee Management System ------------------")
        print("1. Add Employee")
        print("2. View Employee")
        print("3. Update Salary")
        print("4. Search by Department")
        print("5. Delete Employee")
        print("6. Export csv")
        print("7. Import csv")
        print("8. Export JSON")
        print("9. Import JSON")
        print("10. Exit")

        ch = int(input("Enter your choice:"))

        if ch == 1: EmployeeManager.add_employee()
        elif ch == 2: EmployeeManager.view_employees()
        elif ch == 3: EmployeeManager.update_salary()
        elif ch == 4: EmployeeManager.search_by_department()
        elif ch == 5: EmployeeManager.delete_employee()
        elif ch == 6: EmployeeManager.export_csv()
        elif ch == 7: EmployeeManager.import_csv()
        elif ch == 8: EmployeeManager.export_json()
        elif ch == 9: EmployeeManager.import_json()
        elif ch == 10: 
            print("exit...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()