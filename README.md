# Dynamic API

This API provides dynamic management of databases and tables. You can create, delete, list, and update databases and tables. Additionally, it allows for data insertion, updates, and deletion in a flexible way.

## Getting Started

Server should run automatically when starting a workspace. To run manually, run:
```sh
./devserver.sh
```
# API Documentation

### **1. Database Endpoints**

#### 1.1 Create Database

- **URL:** `/db/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "name": "testdb"
  }
  ```
- **Description:** Creates a new database with the given name.

#### 1.2 Delete Database

- **URL:** `/db/<db_name>`
- **Method:** `DELETE`
- **Request Body:**
  ```json
  {
    "db_name": "thetest"
  }
  ```
- **Description:** Deletes the specified database.

#### 1.3 List Databases

- **URL:** `/db`
- **Method:** `GET`
- **Request Body:**
  ```json
  {
    "question": "how to add three numbers"
  }
  ```
- **Description:** Lists all databases present in the system.

#### 1.4 List Tables

- **URL:** `/db/<db_name>`
- **Method:** `GET`
- **Description:** Lists all tables present in the specified database.

---

### **2. Table Endpoints**

#### 2.1 Create Table

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "columns": [
      {"name": "name", "type": "TEXT"},
      {"name": "email", "type": "TEXT"},
      {"name": "age", "type": "INTEGER"},
      {"name": "created_at", "type": "DATETIME"}
    ]
  }
  ```
- **Description:** Creates a new table in the specified database with the provided columns.

#### 2.2 Table Details

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `GET`
- **Description:** Retrieves the details of the specified table.

#### 2.3 Delete Table

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `DELETE`
- **Description:** Deletes the specified table.

#### 2.4 Alter Table

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `PUT`
- **Request Body:**
  ```json
  {
    "add_column": [
      {"name": "created_at", "type": "DATE"},
      {"name": "address", "type": "TEXT"}
    ],
    "remove_column": ["email", "age"]
  }
  ```
- **Description:** Modifies the structure of an existing table by adding or removing columns.

#### 2.5 Rename Column

- **URL:** `/db/<db_name>/<table_name>/rename_column`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "old_column_name": "address",
    "new_column_name": "address2"
  }
  ```
- **Description:** Renames a column in a table.

#### 2.6 Rename Table

- **URL:** `/db/<db_name>/<table_name>/rename`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "new_table_name": "users2"
  }
  ```
- **Description:** Renames a table in the specified database.

---

### **3. Operation Endpoints**

#### 3.1 Update Data

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `PUT`
- **Request Body:**
  ```json
  {
    "update": { "dob": "23rd May 1990" },
    "where": { "age": 28 }
  }
  ```
- **Description:** Updates rows in the specified table based on the given condition.

#### 3.2 Delete Data

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `DELETE`
- **Request Body:**
  ```json
  {
    "where": { "email": "john@example.com" }
  }
  ```
- **Description:** Deletes rows from the table where the condition matches.

#### 3.3 Insert Data

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "data": [
      {"name": "John Doe", "age": 30, "email": "john@example.com", "address": "delhi"},
      {"name": "Jane Doe", "age": 28, "email": "jane@example.com"}
    ]
  }
  ```
- **Description:** Inserts data into the specified table.

#### 3.4 Get Data

- **URL:** `/db/<db_name>/<table_name>`
- **Method:** `GET`
- **Description:** Retrieves data from the specified table.

---

## Example Usage

### **Create a New Database**

```bash
curl -X POST http://127.0.0.1:5000/db/ -d '{"name": "testdb"}' -H "Content-Type: application/json"
```

### **Create a New Table**

```bash
curl -X POST http://127.0.0.1:5000/db/testdb/users -d '{
  "columns": [
    {"name": "name", "type": "TEXT"},
    {"name": "email", "type": "TEXT"},
    {"name": "age", "type": "INTEGER"},
    {"name": "created_at", "type": "DATETIME"}
  ]
}' -H "Content-Type: application/json"
```

### **Insert Data**

```bash
curl -X POST http://127.0.0.1:5000/db/testdb/users -d '{
  "data": [
    {"name": "John Doe", "age": 30, "email": "john@example.com", "address": "delhi"},
    {"name": "Jane Doe", "age": 28, "email": "jane@example.com"}
  ]
}' -H "Content-Type: application/json"
```

---

## Response Format

The API generally responds with a JSON object containing the result of the request. For example, a successful database creation request would return:

```json
{
  "message": "Database 'testdb' created successfully."
}
```

In the case of errors, the response might look like this:

```json
{
  "error": "Database creation failed. Name already exists."
}
```

---

## Conclusion

This API offers dynamic operations on databases and tables with a variety of actions including creation, deletion, data management, and structure modifications. You can interact with it through the described HTTP methods and request bodies.

For detailed testing and usage, you can import this collection into Postman for easy access to all available API calls.

