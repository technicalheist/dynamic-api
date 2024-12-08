import sqlite3
import os

DB_FOLDER = "databases"

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

def create_db(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if os.path.exists(db_path):
        return {"error": f"Database {db_name} already exists"}, 400

    sqlite3.connect(db_path).close()
    return {"message": f"Database {db_name} created successfully"}

def delete_db(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    os.remove(db_path)
    return {"message": f"Database {db_name} deleted successfully"}

def create_table(db_name, table_name, columns):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    # Ensure the 'id' column exists and is primary key with auto-increment
    id_column = {"name": "id", "type": "INTEGER", "primary_key": True, "autoincrement": True}
    id_present = any(col['name'] == "id" for col in columns)

    if id_present:
        for col in columns:
            if col['name'] == "id":
                col.update(id_column)
    else:
        columns.insert(0, id_column)

    # Create column definitions
    column_definitions = ", ".join(
        [f"{col['name']} {col['type']}" +
         (" PRIMARY KEY AUTOINCREMENT" if col.get("primary_key") and col.get("autoincrement") else
          " PRIMARY KEY" if col.get("primary_key") else "")
         for col in columns]
    )
    sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"

    # Execute the SQL query
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()
    conn.close()

    return {"message": f"Table {table_name} created successfully in database {db_name}"}

def alter_table_add_column(db_name, table_name, new_column):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    sql_query = f"ALTER TABLE {table_name} ADD COLUMN {new_column['name']} {new_column['type']}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        conn.commit()
    except sqlite3.OperationalError as e:
        return {"error": str(e)}, 400
    finally:
        conn.close()

    return {"message": f"Column {new_column['name']} added to table {table_name} in database {db_name}"}

def alter_table_remove_column(db_name, table_name, column_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get the table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        if column_name not in column_names:
            return {"error": f"Column {column_name} does not exist in table {table_name}"}, 404

        # Recreate the table without the specified column
        remaining_columns = [col for col in columns if col[1] != column_name]
        remaining_column_names = [col[1] for col in remaining_columns]

        # Generate the SQL queries for creating the new table and migrating data
        create_table_sql = f"""
        CREATE TABLE {table_name}_new (
            {', '.join([f"{col[1]} {col[2]}" for col in remaining_columns])}
        )
        """
        insert_data_sql = f"""
        INSERT INTO {table_name}_new ({', '.join(remaining_column_names)})
        SELECT {', '.join(remaining_column_names)} FROM {table_name}
        """
        drop_old_table_sql = f"DROP TABLE {table_name}"
        rename_table_sql = f"ALTER TABLE {table_name}_new RENAME TO {table_name}"

        # Execute the queries
        cursor.execute(create_table_sql)
        cursor.execute(insert_data_sql)
        cursor.execute(drop_old_table_sql)
        cursor.execute(rename_table_sql)

        conn.commit()
    except sqlite3.OperationalError as e:
        return {"error": str(e)}, 400
    finally:
        conn.close()

    return {"message": f"Column {column_name} removed from table {table_name} in database {db_name}"}

def truncate_table(db_name, table_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    sql_query = f"DELETE FROM {table_name}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        conn.commit()
    except sqlite3.OperationalError as e:
        return {"error": str(e)}, 400
    finally:
        conn.close()

    return {"message": f"Table {table_name} in database {db_name} truncated successfully"}

def delete_table(db_name, table_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    sql_query = f"DROP TABLE IF EXISTS {table_name}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()
    conn.close()

    return {"message": f"Table {table_name} in database {db_name} deleted successfully"}

def list_databases():
    return {"databases": [db[:-3] for db in os.listdir(DB_FOLDER) if db.endswith(".db")]}

def list_tables(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"tables": tables}

def table_details(db_name, table_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
    if not os.path.exists(db_path):
        return {"error": f"Database {db_name} does not exist"}, 404

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [{"name": row[1], "type": row[2]} for row in cursor.fetchall()]
        conn.close()
        return {"columns": columns}
    except sqlite3.OperationalError:
        conn.close()
        return {"error": f"Table {table_name} does not exist in {db_name}"}, 404

def rename_table(db_name, old_table_name, new_table_name):
    try:
        conn = sqlite3.connect(f"{DB_FOLDER}/{db_name}.db")
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {old_table_name} RENAME TO {new_table_name}")
        conn.commit()
        conn.close()
        return {"message": f"Table {old_table_name} renamed to {new_table_name} in database {db_name}"}
    except Exception as e:
        return {"error": str(e)}

def rename_column(db_name, table_name, old_column_name, new_column_name):
    try:
        # Open the database connection
        conn = sqlite3.connect(f"{DB_FOLDER}/{db_name}.db")
        cursor = conn.cursor()

        # Retrieve the table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Log columns for debugging
        print(f"Columns in table {table_name}: {columns}")

        # Initialize flag to check if the column exists
        column_found = False

        # Initialize list for column definitions for the new table
        column_defs = []

        # Iterate through each column and build the new table definition
        for column in columns:
            column_name = column[1].strip()  # Normalize column name (remove extra spaces)
            column_type = column[2]
            column_default = column[4]
            column_notnull = column[3]

            # Check if the current column matches the old column name
            if column_name.lower() == old_column_name.strip().lower():  # Case insensitive check
                column_defs.append(f"{new_column_name} {column_type}")
                column_found = True
            else:
                # Retain other columns as they are
                if column_notnull == 1:
                    column_defs.append(f"{column_name} {column_type} NOT NULL")
                else:
                    column_defs.append(f"{column_name} {column_type}")
            
            # Include default value if there is one
            if column_default is not None:
                column_defs[-1] += f" DEFAULT {column_default}"

        # If the column wasn't found, return an error
        if not column_found:
            return {"error": f"Column {old_column_name} does not exist in table {table_name}"}

        # Prepare the column definitions string for the new table
        column_defs_str = ", ".join(column_defs)

        # Log the CREATE TABLE query for debugging
        print(f"CREATE TABLE query: CREATE TABLE {table_name}_new ({column_defs_str})")

        # Create the new table with the updated column name
        new_table_name = f"{table_name}_new"
        cursor.execute(f"CREATE TABLE {new_table_name} ({column_defs_str})")

        # Copy data from the old table to the new table
        cursor.execute(f"INSERT INTO {new_table_name} SELECT * FROM {table_name}")

        # Drop the old table
        cursor.execute(f"DROP TABLE {table_name}")

        # Rename the new table to the original table name
        cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO {table_name}")

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        return {"message": f"Column {old_column_name} renamed to {new_column_name} in table {table_name} in database {db_name}"}
    
    except sqlite3.Error as e:
        return {"error": f"SQLite error: {str(e)}"}

def truncate_table(db_name, table_name):
    try:
        conn = sqlite3.connect(f"{DB_FOLDER}/{db_name}.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        conn.close()
        return {"message": f"Table {table_name} truncated in database {db_name}"}
    except Exception as e:
        return {"error": str(e)}
