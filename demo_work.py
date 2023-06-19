"""
    import SQLite 3
    and from import datetime import datetime, timedelta
"""
import sqlite3
from datetime import datetime, timedelta

# Create the database connection
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create the product table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        name TEXT,
        price REAL,
        quantity INTEGER,
        date_added TEXT
    )
""")

# Function to add a product to the database
def add_product(category, name, price, quantity, date_added):
    """ Null value check 
        Convert price and quantity to numeric values
    """
    # Convert price and quantity to numeric values
    try:
        price = float(price)
        quantity = float(quantity)
    except ValueError:
        print("Error: Invalid price or quantity.")
        return
    # Insert the product into the database
    cursor.execute("""
        INSERT INTO products (category, name, price, quantity, date_added)
        VALUES (?, ?, ?, ?, ?)
    """, (category, name, price, quantity, date_added))
    conn.commit()
    print("Product added to the inventory.")
# Validate the value
def validate_date(value):
    """ Validate date
        read time specific format
    """
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False
# Validate float value
def validate_float(value):
    """
        Validate float value
        or except value error
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
# Validate positive float value
def validate_positive_float(value):
    """
        Check float value positive
        and also check grater than or equal
    """
    if validate_float(value) and float(value) >= 1:
        return True
    return False
# Check duplicates Enter or not
def check_duplicate(category, name,price, quantity, date_added):
    """
        All value duplicate will not accept 
        error print existing product
    """
    cursor.execute('SELECT * FROM products WHERE category = ? AND name = ? AND price=? AND quantity=? AND date_added=?', (category, name,price, quantity, date_added))
    return cursor.fetchone() is not None

# Filter category
def filter_by_category(category):
    """
    Function to filter products by category.
    fetch all from memory to print result
    and display the products
    """
    cursor.execute("SELECT * FROM products WHERE category=?", (category,))
    products = cursor.fetchall()
    display_products(products)

# Filter product_name
def filter_by_product_name(product_name):
    """
    Function to filter products by product name
    fetch all from memory to print result
    and display the products
    """
    cursor.execute("SELECT * FROM products WHERE name=?", (product_name,))
    products = cursor.fetchall()
    display_products(products)

# Filter by date
def filter_by_date_added(days):
    """
    Function to filter products by date added
    fetch all from memory to print result
    and display the product
    """
    date_limit = datetime.now() - timedelta(days=days)
    cursor.execute(
        "SELECT * FROM products WHERE date_added < ?", (date_limit.strftime("%Y-%m-%d"),))
    products = cursor.fetchall()
    display_products(products)

# Display products
def display_products(products):
    """
    Function to display filtered products
    else no products found
    """
    if products:
        print("Filtered Products:")
        for product in products:
            print(
                f"Category: {product[1]}",
                f"Name: {product[2]}",
                f"Price: {product[3]}",
                f"Quantity: {product[4]}",
                f"Date Added: {product[5]}")
    else:
        print("No products found.")

# Display inventory
def display_inventory():
    """
        Added products 
        Function to display current inventory
    """
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    if products:
        print("Current Inventory:")
        for product in products:
            print(
                f"Category: {product[1]}",
                f"Name: {product[2]}",
                f"Price: {product[3]}",
                f"Quantity: {product[4]}",
                f"Date Added: {product[5]}")
    else:
        print("Inventory is empty.")
# Select the choice and give user input detail
def main():
    """
        Main function to run the program
        Choosing the choice
    """
    while True:
        print("\n1. Add product")
        print("2. Filter by category")
        print("3. Filter by product name")
        print("4. Filter by date added")
        print("5. Display inventory")
        print("6. Quit")

        choice = input("Enter your choice: ")
        # select choice 1
        if choice == "1":
            while True:
                category = input("Enter category name: ")
                if not category:
                    print("Error: Category name cannot be empty")
                    continue
                break
            while True:
                name = input("Enter product name: ")
                if not name:
                    print("Error: Product name cannot be empty")
                    continue
                break
            while True:
                price = input("Enter unit price: ")
                if not price or not validate_positive_float(price):
                    print("Error: price name cannot be empty and must be a positive float value")
                    continue
                break
            while True:
                quantity = input("Enter quantity: ")
                if not quantity or not validate_positive_float(quantity):
                    print("Error: quantity cannot be empty. Quantity must be a positive float value")
                    continue
                break
            while True:
                date_added = input("Enter date added (yyyy-mm-dd): ")
                if not date_added or not validate_date(date_added):
                    print("Error: Invalid date format. Please use yyyy-MM-dd")
                    continue
                break
            if check_duplicate(category, name,price, quantity, date_added):
                print("existing product")
                continue

            add_product(category, name, price, quantity, date_added)
        # Select choice 2
        elif choice == "2":
            category = input("Enter category name: ")
            filter_by_category(category)
        # Select choice 3
        elif choice == "3":
            product_name = input("Enter product name: ")
            filter_by_product_name(product_name)
        # Select choice 4
        elif choice == "4":
            days = int(input("Enter the number of days: "))
            filter_by_date_added(days)
        # Select choice 5
        elif choice == "5":
            display_inventory()
        # selected choice 6
        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
