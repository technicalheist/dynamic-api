# Flask API Service Starter

This is a minimal Flask API service starter based on [Google Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service).

## Getting Started

Server should run automatically when starting a workspace. To run manually, run:
```sh
./devserver.sh
```
Flask API for Database Management
=====================================
Endpoints
------------
Database Management
POST /create_db: Creates a new database.
POST /delete_db: Deletes a database.
GET /list_databases: Lists all databases.
Table Management
POST /create_table: Creates a new table in a database.
POST /alter_table: Alters a table in a database.
POST /truncate_table: Truncates a table in a database.
POST /delete_table: Deletes a table from a database.
Table Information
GET /list_tables/<db_name>: Lists all tables in a database.
GET /table_details/<db_name>/<table_name>: Retrieves details about a table.
Table Renaming
POST /rename_table: Renames a table in a database.
POST /rename_column: Renames a column in a table.
Database Integrity
POST /check_integrity: Checks the integrity of a database.
Table Constraints
GET /table_constraints: Retrieves the constraints of a table.
Record Operations
GET /<db_name>/<table_name>: Retrieves data from a table.
POST /<db_name>/<table_name>: Inserts data into a table.
PUT /<db_name>/<table_name>: Updates data in a table.
DELETE /<db_name>/<table_name>: Deletes data from a table.
GET /<db_name>/<table_name>/<id>: Retrieves a record by its ID.
PUT /<db_name>/<table_name>/<id>: Updates a record by its ID.
DELETE /<db_name>/<table_name>/<id>: Deletes a record by its ID.
Raw SQL Query Execution
POST /sql: Executes a raw SQL query against a specific database.