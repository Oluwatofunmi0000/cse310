# Simulate a cloud database connection (for Cloud Databases module)
def connect_to_cloud_database():
	"""
	Simulate connecting to a cloud database service.
	In a real-world scenario, this would use a cloud provider's SDK or connection string.
	For example, connecting to AWS RDS, Azure SQL, or Google Cloud SQL.

	Example for Azure SQL Database (using pyodbc):
		import pyodbc
		conn = pyodbc.connect(
			'DRIVER={ODBC Driver 17 for SQL Server};'
			'SERVER=your_server.database.windows.net;'
			'DATABASE=your_db;UID=your_user;PWD=your_password'
		)

	Example for AWS RDS (using pymysql):
		import pymysql
		conn = pymysql.connect(
			host='your-rds-endpoint',
			user='your_user',
			password='your_password',
			database='your_db'
		)

	For this project, we use SQLite locally for demonstration.
	"""
	print("Connecting to cloud database... (simulation)")
	# Place real cloud connection code here for production use
	return True
"""
hello_world.py

A simple Python web app simulation with database interaction and comments for educational purposes.
"""

"""
hello_world.py

MongoDB Atlas cloud database CLI demo with two related collections: users and greetings.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# Replace <db_password> with your actual password
MONGO_URI = "mongodb+srv://JoyOyaleke:oluwatofunmi@clustercse341.0tc5kdx.mongodb.net/?appName=ClusterCSE341"
DB_NAME = "cloud_demo"

def get_db():
	"""Connect to MongoDB Atlas and return the database object."""
	client = MongoClient(MONGO_URI)
	db = client[DB_NAME]
	return db

def print_menu():
	print("\nMenu:")
	print("1. Add User")
	print("2. Add Greeting for User")
	print("3. View All Users")
	print("4. View Greetings for User")
	print("5. Update Greeting")
	print("6. Delete Greeting")
	print("7. Exit")

def add_user(db):
	name = input("Enter user name: ")
	email = input("Enter user email: ")
	user = {"name": name, "email": email, "created_at": datetime.now()}
	result = db.users.insert_one(user)
	print(f"User added with id: {result.inserted_id}")

def add_greeting(db):
	user_id = input("Enter user id for greeting: ")
	message = input("Enter greeting message: ")
	greeting = {
		"user_id": ObjectId(user_id),
		"message": message,
		"created_at": datetime.now()
	}
	result = db.greetings.insert_one(greeting)
	print(f"Greeting added with id: {result.inserted_id}")

def view_users(db):
	print("\nAll Users:")
	for user in db.users.find():
		print(f"{user['_id']}: {user['name']} ({user['email']})")

def view_greetings_for_user(db):
	user_id = input("Enter user id to view greetings: ")
	print(f"\nGreetings for user {user_id}:")
	for greeting in db.greetings.find({"user_id": ObjectId(user_id)}):
		print(f"{greeting['_id']}: {greeting['message']} (at {greeting['created_at']})")

def update_greeting(db):
	greeting_id = input("Enter greeting id to update: ")
	new_message = input("Enter new message: ")
	result = db.greetings.update_one(
		{"_id": ObjectId(greeting_id)},
		{"$set": {"message": new_message}}
	)
	if result.modified_count:
		print("Greeting updated.")
	else:
		print("Greeting not found or not updated.")

def delete_greeting(db):
	greeting_id = input("Enter greeting id to delete: ")
	result = db.greetings.delete_one({"_id": ObjectId(greeting_id)})
	if result.deleted_count:
		print("Greeting deleted.")
	else:
		print("Greeting not found.")

def main():
	db = get_db()
	print("Connected to MongoDB Atlas cloud database!\n")
	while True:
		print_menu()
		choice = input("Enter your choice: ")
		if choice == '1':
			add_user(db)
		elif choice == '2':
			add_greeting(db)
		elif choice == '3':
			view_users(db)
		elif choice == '4':
			view_greetings_for_user(db)
		elif choice == '5':
			update_greeting(db)
		elif choice == '6':
			delete_greeting(db)
		elif choice == '7':
			print("Exiting app.")
			break
		else:
			print("Invalid choice. Try again.")

if __name__ == "__main__":
	main()
