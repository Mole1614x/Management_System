import sqlite3
import os


""" @staticmethod: A static method in Python is a method inside a class that does not depend on instance (object) data or class data. It behaves like a normal function, but is grouped inside the class for logical organization. """



class DatabaseManager:
    #--------------------------- Database -----------------------------------------#
    conn = sqlite3.connect("ecommerce.db", isolation_level=None)
    cursor = conn.cursor()
    # Enable foreign keys
    #cursor.execute("PRAGMA foreign_keys = ON")

    #--------------------------- Table Creation ----------------------------------#
    cursor.execute("""create table if not exists users( user_id integer primary key autoincrement , username text, password text) """)

    cursor.execute("""create table if not exists products(product_id integer primary key autoincrement , name text, price real, stock integer)""")

    cursor.execute("""create table if not exists cart(cart_id integer primary key autoincrement, user_id integer, product_id integer, quantity integer, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(product_id) REFERENCES products(product_id) )""")

    cursor.execute("""create table if not exists orders(order_id integer primary key autoincrement, user_id integer, total_price real, order_date text, FOREIGN KEY(user_id) REFERENCES users(user_id)) """)

    #------------------------------- clear table Testing purpose --------------------------------#

    cursor.execute("delete from users")
    cursor.execute("delete from products")
    cursor.execute("delete from cart")

    #-------------------------------- Remove auto increment-----------------------#

    cursor.execute("delete from sqlite_sequence where name = 'users'")
    cursor.execute("delete from sqlite_sequence where name = 'products'")
    cursor.execute("delete from sqlite_sequence where name = 'cart'")


#--------------------------------- Login System -------------------------------#
class user:

    @staticmethod
    def register():

        username = input("Enter your username:").strip().lower()
        password = input("Enter your password:")

        with open("user.txt", "a") as f:
            f.write(f"{username},{password}\n")

        print("Registered Successfully!")

    @staticmethod
    def login():

        username = input("Enter username: ").strip().lower()
        password = input("Enter password: ")

        if not os.path.exists("user.txt"):
            open("user.txt", "w").close()

        with open("user.txt","r") as f:
            users = f.readlines()

        for user in users:
            u,p = user.strip().split(",")

            if u == username and p == password: 
                print("Login Successful!")
                return True
        print("Invalid Credentials!")
        return False
    
    @staticmethod
    def login_system():

        attempts = 3
        while attempts > 0:
            if user.login():
                return True
            else:
                attempts -= 1
                print(f"Attempts Left: {attempts}")
        print("Too many failed attempts!")
        return False

#------------------------------- Product Management   ---------------------------------------#

class Product:

    @staticmethod
    def admin_add_product(is_admin):
        if is_admin:
            Product.add_product()
        else:
            print("Access Denied! Admin Only!")        # is_admin = True parameter passing 

    @staticmethod
    def add_product():

        name = input("Enter your product name:") 
        price = int(input("Enter your product price:"))
        stock = int(input("Enter your product stock:")) 

        DatabaseManager.cursor.execute("insert into products(name,price,stock) values(?,?,?)",(name,price,stock))

        print("Product Added Successfully!")

    @staticmethod
    def view_product():

        DatabaseManager.cursor.execute("select * from products")
        products = DatabaseManager.cursor.fetchall()

        if not products:
            print("No products available!")
            return
        print("\n-------- Product List ---------")
        for p in products:
            print(f"ID: {p[0]} | Name: {p[1]} | Price: {p[2]} | Stock: {p[3]}")

    @staticmethod
    def show_stock():
        print("----- Stock Availability --------")
        DatabaseManager.cursor.execute("select name,stock from products")
        products = DatabaseManager.cursor.fetchall()

        if not products:
            print("No product Found!")
            return

        for name , stock in products:
            if stock > 0:
                status = "In Stock"
            else:
                status = "Out of stock"

            print(f"{name} --> {status} (Qty): {stock}")



#--------------------------- Cart Features ----------------------------#

class Cart:

    @staticmethod
    def add_to_cart(user_id):
        
        print("\n--- Add to Cart ---")
        product_id = int(input("Enter ypur product id:"))
        qty = int(input("Enter quantity to add:"))

        # Check if product Exists

        DatabaseManager.cursor.execute("select name, stock from products where product_id = ?",(product_id,))

        product = DatabaseManager.cursor.fetchone()

        if not  product:
            print("Product does not Exists!")
            return

        name , stock = product

        # Check stock availability

        if stock < qty:
            print(f"Only {stock} items available in stock!")
            return
        
        # check if product already in cart

        DatabaseManager.cursor.execute("select quantity from cart where user_id = ? AND product_id = ?", (user_id,product_id))

        existing = DatabaseManager.cursor.fetchone()

        if existing:
            # update qty

            new_qty = existing[0] + qty

            DatabaseManager.cursor.execute("update cart set quantity = ? where user_id = ? AND product_id =?",(new_qty, user_id, product_id))
        else:
            # Insert new item

            DatabaseManager.cursor.execute("INSERT INTO cart(user_id, product_id, quantity) VALUES (?, ?, ?)",(user_id, product_id, qty))

        print(f"{name} added to cart")

    #-------------------- Remove From Cart -------------------------------#
    @staticmethod
    def remove_from_cart(user_id):

        print("\n--- Remove From Cart ---")
        print("1. Remove using Product ID")
        print("2. Remove using Cart ID")

        ch = int(input("Enter your choice: "))

        if ch == 1:
            product_id = int(input("Enter your product id to remove from cart: "))

            #  FIX 1: Check in cart (not products)
            DatabaseManager.cursor.execute(
                "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )

            item = DatabaseManager.cursor.fetchone()

            if not item:
                print("The product cannot be found!")
                return

            #  Delete item
            DatabaseManager.cursor.execute(
                "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )

            print("Product removed from cart!")

        elif ch == 2:

            cart_id = int(input("Enter your cart_id: "))

            # Check if item exists
            DatabaseManager.cursor.execute(
                "SELECT * FROM cart WHERE cart_id = ? AND user_id = ?",
                (cart_id, user_id)
            )

            item = DatabaseManager.cursor.fetchone()

            if not item:
                print("Item not found!")
                return

            # FIX 2: Actually delete (was missing)
            DatabaseManager.cursor.execute(
                "DELETE FROM cart WHERE cart_id = ? AND user_id = ?",
                (cart_id, user_id)
            )

            print("Item removed from cart!")

        else:
            print("Invalid Choice!")

        
    #------------------------------ View Cart --------------------------------------#

    @staticmethod
    def view_cart(user_id):

        print("--------- Your Cart --------------")

        # JOIN Cart + products

        DatabaseManager.cursor.execute("""select p.name,c.quantity,p.price from cart c join products p on c.product_id = p.product_id where c.user_id = ?""", (user_id,))

        items = DatabaseManager.cursor.fetchall()

        if not items:
            print("Your cart is Empty!")
            return
        
        total_bill = 0

        print("\nName | Qty | Price | Total")
        print("----------------------------")

        for name,qty,price in items:
            total = qty * price
            total_bill += total
            print(f"{name} | {qty} | Rs.{price} | Rs.{total}")

        print("------------------------------------------")
        print(f"Total Bill: Rs.{total_bill}")

class Order:

    @staticmethod
    def checkout(user_id):

        print("----------------Checkout------------")

        # Fetch cart items

        DatabaseManager.cursor.execute("""select c.product_id,p.name,p.price,p.stock,c.quantity from cart c JOIN products p on c.product_id = p.product_id where c.user_id = ?""",(user_id,))

        items = DatabaseManager.cursor.fetchall()

        if not items:
            print("Cart is Empty!")
            return
        
        total_price = 0

        # check stock + calculate total

        for product_id,name,price,stock,qty in items:

            if stock < qty:
                print(f"Not enough stock for {name} (Available: {stock})")
                return
            
            total_price += price * qty

        # Deduct Stock


        for product_id, name, price, stock, qty in items:
            new_stock = stock - qty

            DatabaseManager.cursor.execute("Update products set stock = ? where product_id = ?",(new_stock,product_id))
            
        # Insert into orders


        from datetime import datetime

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        DatabaseManager.cursor.execute("insert into orders(user_id,total_price,order_date) Values (?,?,?)",(user_id,total_price,order_date))


        # Clear Cart

        DatabaseManager.cursor.execute("Delete from cart where user_id = ?", (user_id,))

        print("Order placed Successfully!")
        print(f"Total Paid: Rs.{total_price}")


def main():

    print("============== Bazaar.Com ===============")


    print("1. Register")
    print("2. Login")

    choice = input("Enter choice: ")

    if choice == "1":
        user.register()

    if not user.login_system():
        return
    
    user_id = 1

    while True:

        print("\n===== MAIN MENU =====")
        print("1. Add Product (Admin)")
        print("2. View Products")
        print("3. Show Stock")
        print("4. Add to Cart")
        print("5. View Cart")
        print("6. Remove from Cart")
        print("7. Checkout")
        print("8. Exit")

        choice = int(input("Enter your choice: "))

        #-------------- Product -------------------#

        if choice == 1:
            is_admin = True 
            Product.admin_add_product(is_admin)
        elif choice == 2:
            Product.view_product()
        elif choice == 3:
            Product.show_stock()
        
        #---------------- Cart ---------------------#

        elif choice == 4:
            Cart.add_to_cart(user_id)
        
        elif choice == 5:
            Cart.view_cart(user_id)

        elif choice == 6:
            Cart.remove_from_cart(user_id)

        # ---------------- ORDER ---------------- #
        elif choice == 7:
            Order.checkout(user_id)

        # ---------------- EXIT ---------------- #
        elif choice == 8:
            print("Thank you for using the system 👋")
            break

        else:
            print("❌ Invalid choice! Try again.")


# ---------------- RUN PROGRAM ---------------- #
if __name__ == "__main__":
    main()