products = []
next_id = 1   # auto-increment id

# ---------------- ADD PRODUCT ----------------
def add_product():
    global next_id
    
    name = input("Enter product name: ").strip()
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    
    if quantity < 0:
        print("❌ Quantity cannot be negative!")
        return
    
    product = {
        "id": next_id,
        "name": name,
        "price": price,
        "quantity": quantity
    }
    
    products.append(product)
    next_id += 1
    
    print("✅ Product added successfully!")

# ---------------- VIEW PRODUCTS ----------------
def view_products():
    if not products:
        print("⚠ No products available")
        return
    
    print("\n--- Product List ---")
    for p in products:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: {p['price']} | Qty: {p['quantity']}")

# ---------------- UPDATE QUANTITY ----------------
def update_quantity():
    pid = int(input("Enter product ID: "))
    
    for p in products:
        if p["id"] == pid:
            new_qty = int(input("Enter new quantity: "))
            
            if new_qty < 0:
                print("❌ Quantity cannot be negative!")
                return
            
            p["quantity"] = new_qty
            print("✅ Quantity updated!")
            return
    
    print("❌ Product not found!")

# ---------------- DELETE PRODUCT ----------------
def delete_product():
    pid = int(input("Enter product ID: "))
    
    for p in products:
        if p["id"] == pid:
            products.remove(p)
            print("🗑 Product deleted!")
            return
    
    print("❌ Product not found!")

# ---------------- SEARCH PRODUCT ----------------
def search_product():
    keyword = input("Enter product name to search: ").lower()
    
    found = False
    for p in products:
        if keyword in p["name"].lower():
            print(f"ID: {p['id']} | Name: {p['name']} | Price: {p['price']} | Qty: {p['quantity']}")
            found = True
    
    if not found:
        print("❌ No matching product found!")

# ---------------- MENU ----------------
def menu():
    while True:
        print("\n==== PRODUCT INVENTORY SYSTEM ====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Quantity")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_quantity()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            search_product()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice!")

# Run program
menu()
