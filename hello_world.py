"""
hello_world.py

SQL Relational Database Demo: SQLite CRUD, Join, Aggregates, and Date Filtering
Author: Joy Oyaleke
"""

import sqlite3
from datetime import datetime

DB_NAME = "demo.db"


def connect_db():
    """Connect to the SQLite database (creates file if not exists)."""
    return sqlite3.connect(DB_NAME)


def create_tables(conn):
    """Create users and orders tables."""
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                order_date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)


def insert_user(conn, name, email):
    """Insert a new user into the users table."""
    with conn:
        conn.execute(
            "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
            (name, email, datetime.now().isoformat()),
        )


def insert_order(conn, user_id, amount, order_date):
    """Insert a new order for a user."""
    with conn:
        conn.execute(
            "INSERT INTO orders (user_id, amount, order_date) VALUES (?, ?, ?)",
            (user_id, amount, order_date),
        )


def update_user_email(conn, user_id, new_email):
    """Update a user's email address."""
    with conn:
        conn.execute(
            "UPDATE users SET email = ? WHERE id = ?",
            (new_email, user_id),
        )


def delete_order(conn, order_id):
    """Delete an order by its ID."""
    with conn:
        conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))


def get_all_users(conn):
    """Retrieve and print all users."""
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, created_at FROM users")
    users = cur.fetchall()
    print("\nAll Users:")
    for u in users:
        print(f"ID: {u[0]}, Name: {u[1]}, Email: {u[2]}, Created: {u[3]}")
    return users


def get_orders_for_user(conn, user_id):
    """Retrieve and print all orders for a user."""
    cur = conn.cursor()
    cur.execute("SELECT id, amount, order_date FROM orders WHERE user_id = ?", (user_id,))
    orders = cur.fetchall()
    print(f"\nOrders for User {user_id}:")
    for o in orders:
        print(f"Order ID: {o[0]}, Amount: {o[1]}, Date: {o[2]}")
    return orders


def join_users_orders(conn):
    """Perform a join between users and orders and print results."""
    cur = conn.cursor()
    cur.execute("""
        SELECT users.name, orders.amount, orders.order_date
        FROM users
        JOIN orders ON users.id = orders.user_id
    """)
    results = cur.fetchall()
    print("\nUser Orders (Join):")
    for r in results:
        print(f"User: {r[0]}, Amount: {r[1]}, Date: {r[2]}")
    return results


def aggregate_order_stats(conn):
    """Use aggregate functions to summarize order data."""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), AVG(amount), SUM(amount) FROM orders")
    count, avg, total = cur.fetchone()
    print(f"\nOrder Stats: Total Orders: {count}, Average Amount: {avg}, Total Amount: {total}")
    return count, avg, total


def filter_orders_by_date(conn, start_date, end_date):
    """Filter orders within a date range."""
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, amount, order_date FROM orders WHERE order_date BETWEEN ? AND ?",
        (start_date, end_date),
    )
    results = cur.fetchall()
    print(f"\nOrders from {start_date} to {end_date}:")
    for r in results:
        print(f"Order ID: {r[0]}, User ID: {r[1]}, Amount: {r[2]}, Date: {r[3]}")
    return results


def print_menu():
    """Print the main menu."""
    print("\n=== SQL Relational Database Demo ===")
    print("If you do not see the menu, your terminal may not support interactive input.\n")
    print("Menu:")
    print("1. Add User")
    print("2. Add Order for User")
    print("3. View All Users")
    print("4. View Orders for User")
    print("5. Update User Email")
    print("6. Delete Order")
    print("7. Join: List All User Orders")
    print("8. Aggregate: Order Stats")
    print("9. Filter Orders by Date Range")
    print("10. Exit")


def parse_int_input(prompt):
    """Prompt the user for an integer; allow commas and whitespace, retry until valid."""
    while True:
        raw = input(prompt)
        if raw is None:
            print("No input provided.")
            continue
        clean = raw.strip().replace(',', '').replace(' ', '')
        try:
            return int(clean)
        except ValueError:
            print("Invalid integer. Please enter a numeric value (commas allowed).")


def parse_float_input(prompt):
    """Prompt the user for a float; allow commas and whitespace, retry until valid."""
    while True:
        raw = input(prompt)
        if raw is None:
            print("No input provided.")
            continue
        clean = raw.strip().replace(',', '').replace(' ', '')
        try:
            return float(clean)
        except ValueError:
            print("Invalid number. Please enter a numeric value (commas allowed).")


def main():
    """Main program loop for SQL database demo."""
    conn = connect_db()
    create_tables(conn)
    while True:
        print_menu()
        import sys
        sys.stdout.flush()
        try:
            choice = input("Enter choice: ")
        except Exception as e:
            print(f"ERROR: Exception during input(): {e}")
            break
        if choice == "1":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            try:
                insert_user(conn, name, email)
                print("User added.")
            except sqlite3.IntegrityError:
                print("That email is already in use. Please enter a different email.")
        elif choice == "2":
            users = get_all_users(conn)
            user_id = parse_int_input("Enter user ID for order: ")
            amount = parse_float_input("Enter order amount: ")
            order_date = input("Enter order date (YYYY-MM-DD): ")
            insert_order(conn, user_id, amount, order_date)
            print("Order added.")
        elif choice == "3":
            get_all_users(conn)
        elif choice == "4":
            user_id = parse_int_input("Enter user ID to view orders: ")
            get_orders_for_user(conn, user_id)
        elif choice == "5":
            user_id = parse_int_input("Enter user ID to update email: ")
            new_email = input("Enter new email: ")
            try:
                update_user_email(conn, user_id, new_email)
                print("User email updated.")
            except sqlite3.IntegrityError:
                print("That email is already in use. Please enter a different email.")
        elif choice == "6":
            order_id = parse_int_input("Enter order ID to delete: ")
            delete_order(conn, order_id)
            print("Order deleted.")
        elif choice == "7":
            join_users_orders(conn)
        elif choice == "8":
            aggregate_order_stats(conn)
        elif choice == "9":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            filter_orders_by_date(conn, start_date, end_date)
        elif choice == "10":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")
    conn.close()


if __name__ == '__main__':
    main()
