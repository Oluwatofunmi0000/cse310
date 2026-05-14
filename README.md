# Cloud Databases: Overview and Implementation

A **cloud database** is a database service built and accessed through a cloud platform. Cloud databases offer scalability, high availability, and remote access, making them ideal for modern web and enterprise applications. Examples include AWS RDS, Azure SQL Database, and Google Cloud SQL.

## How This Project Simulates a Cloud Database

This project demonstrates the core concepts of connecting to and interacting with a database, simulating a cloud database connection in the code. The `connect_to_cloud_database()` function in the code represents where you would connect to a real cloud database using a provider's SDK or connection string. For demonstration, the app uses SQLite locally, but the structure and logic can be adapted for any cloud database.

### Example: Adapting to a Real Cloud Database

To use a real cloud database, you would replace the SQLite connection with a connection string for your cloud provider. For example:

```
# Example for Azure SQL Database (using pyodbc):
# import pyodbc
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server.database.windows.net;DATABASE=your_db;UID=your_user;PWD=your_password')
```

This approach allows your application to scale and be accessed from anywhere, leveraging the benefits of cloud infrastructure.

# Overview

This project demonstrates a simple Python program that prints "Hello World" to the screen. The goal is to practice basic software development skills and further my learning as a software engineer by building, documenting, and sharing a simple application.

This software was created to reinforce my understanding of the development workflow, including coding, documentation, version control, and video demonstration.

[Software Demo Video](https://youtu.be/dCwtUeSMUz0)

(github link) [https://github.com/Oluwatofunmi0000/cse310]

# Cloud Database Integration (Simulation)

This project simulates connecting to a cloud database as part of the Cloud Databases module requirement. In a real-world scenario, the app could connect to a cloud database service such as AWS RDS, Azure SQL Database, or Google Cloud SQL by using the appropriate SDK or connection string. For demonstration and simplicity, this project uses SQLite locally, but the code includes a function (`connect_to_cloud_database`) to show where and how a cloud connection would be established.

# Development Environment

## Module Selection

The following module was selected and completed for this project:

- [x] Cloud Databases
- [ ] Data Analysis
- [ ] Game Framework
- [ ] GIS Mapping
- [ ] Mobile App
- [ ] Networking
- [ ] SQL Relational Databases
- [ ] Web Apps
- [ ] Language – C++
- [ ] Language – Java
- [ ] Language – Kotlin
- [ ] Language – R
- [ ] Language – Erlang
- [ ] Language – JavaScript
- [ ] Language – C#
- [ ] Language – TypeScript
- [ ] Language – Rust

- Visual Studio Code
- Git
- Python 3.x

# Programming Language

Python

# Useful Websites

- [Python Official Documentation](https://docs.python.org/3/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Guides](https://guides.github.com/)

# Author

Joy Oyaleke

# Time Spent

20 hours

# Learning Strategies

To complete this module, I used the following learning strategies:

- Reviewed official Python and SQLite documentation
- Watched online tutorials on database and web app basics
- Practiced by writing and testing code examples
- Sought help from peers and online forums when stuck
- Broke the project into smaller tasks and set goals for each session
