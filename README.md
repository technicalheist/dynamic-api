# Dynamic API

This API provides endpoints to manage databases, tables, and records. It includes features for database creation, table management, data manipulation, and execution of raw SQL queries.


## Getting Started

Server should run automatically when starting a workspace. To run manually, run:
```sh
./devserver.sh
```
# API Documentation

## Overview
This API provides endpoints to manage databases, tables, and records. It includes features for database creation, table management, data manipulation, and execution of raw SQL queries.

---

## Endpoints

### Database Management
- **POST /create_db**  
  Creates a new database.

- **POST /delete_db**  
  Deletes a specified database.

- **GET /list_databases**  
  Lists all available databases.

---

### Table Management
- **POST /create_table**  
  Creates a new table in a specified database.

- **POST /alter_table**  
  Alters the structure of a table in a database.

- **POST /truncate_table**  
  Removes all records from a table in a database.

- **POST /delete_table**  
  Deletes a table from a specified database.

---

### Table Information
- **GET /list_tables/<db_name>**  
  Lists all tables in the specified database.

- **GET /table_details/<db_name>/<table_name>**  
  Retrieves detailed information about a specified table in a database.

---

### Table Renaming
- **POST /rename_table**  
  Renames a table in a database.

- **POST /rename_column**  
  Renames a column in a specified table.

---

### Database Integrity
- **POST /check_integrity**  
  Checks the integrity of a specified database.

---

### Table Constraints
- **GET /table_constraints**  
  Retrieves the constraints (e.g., primary keys, foreign keys) of a specified table.

---

### Record Operations
- **GET /<db_name>/<table_name>**  
  Retrieves all data from a specified table.

- **POST /<db_name>/<table_name>**  
  Inserts new data into a specified table.

- **PUT /<db_name>/<table_name>**  
  Updates existing data in a specified table.

- **DELETE /<db_name>/<table_name>**  
  Deletes data from a specified table.

- **GET /<db_name>/<table_name>/**  
  Retrieves a record by its ID.

- **PUT /<db_name>/<table_name>/**  
  Updates a record by its ID.

- **DELETE /<db_name>/<table_name>/**  
  Deletes a record by its ID.

---

### Raw SQL Query Execution
- **POST /sql**  
  Executes a raw SQL query against a specified database.

---

## Usage Notes
- Replace `<db_name>` and `<table_name>` with the names of the database and table respectively when using the endpoints.
- Use appropriate HTTP methods (GET, POST, PUT, DELETE) for the desired operation.
- Ensure valid data formats for insert and update operations.
- Permissions and constraints of the database and tables apply during all operations.

## Error Handling
- Standard HTTP status codes are used:
  - **200**: Successful operation
  - **400**: Bad request
  - **404**: Resource not found
  - **500**: Internal server error

--- 
