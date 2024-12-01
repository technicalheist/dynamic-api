import sqlite3
from flask import jsonify

DB_FOLDER = "databases"

# Helper function to execute a query and return results
def execute_query(db_name, query, params=None, fetch=False):
    try:
        conn = sqlite3.connect(f"{DB_FOLDER}/{db_name}.db")
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {"message": "Query executed successfully"}
        conn.close()
        return result
    except sqlite3.Error as e:
        return {"error": str(e)}

# Helper function to check if a table exists in the database
def table_exists(db_name, table_name):
    try:
        conn = sqlite3.connect(f"{DB_FOLDER}/{db_name}.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        table = cursor.fetchone()
        conn.close()
        return bool(table)
    except sqlite3.Error as e:
        return {"error": str(e)}


# Insert data into a table
def insert_data(db_name, table_name, data):
    try:
        if isinstance(data, dict):
            data = [data]

        for row in data:
            if "id" in row:
                del row["id"]

        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['?'] * len(data[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        for row in data:
            values = tuple(row.values())
            execute_query(db_name, query, values)
        
        return {"message": "Records inserted successfully"}
    except sqlite3.Error as e:
        print(str(e))
        return {"error": str(e)}



# Update data in a table
def update_data(db_name, table_name, update_values, where_conditions):
    try:
        set_clause = ', '.join([f"{key} = ?" for key in update_values.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in where_conditions.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        
        params = tuple(update_values.values()) + tuple(where_conditions.values())
        execute_query(db_name, query, params)
        
        return {"message": "Record updated successfully"}
    except sqlite3.Error as e:
        return {"error": str(e)}

# Delete data from a table
def delete_data(db_name, table_name, where_conditions):
    try:
        where_clause = ' AND '.join([f"{key} = ?" for key in where_conditions.keys()])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        
        params = tuple(where_conditions.values())
        execute_query(db_name, query, params)
        
        return {"message": "Record(s) deleted successfully"}
    except sqlite3.Error as e:
        return {"error": str(e)}


def parse_where_conditions(args):
    conditions = []
    values = []
    
    # Loop through the query parameters to identify where conditions
    for key, value in args.items():
        if key.endswith("_IN"):
            column = key.replace("_IN", "")
            values = value.strip("[]").split(",")  # Parse the array for IN condition
            conditions.append(f"{column} IN ({','.join(['?' for _ in values])})")
            values.extend(values)
        elif key != 'limit' and key != 'start' and key != 'order' and key != 'orderby':  # Skip pagination and ordering params
            column = key
            conditions.append(f"{column} = ?")
            values.append(value)

    where_clause = " AND ".join(conditions)
    return where_clause, values

def fetch_data(db_name, table_name, limit=10, start=0, order_by="id", order="ASC", where_clause=None, where_values=None):
    try:
        where_condition = ""
        values = []

        # Handle WHERE condition
        if where_clause and where_values:
            where_condition = f"WHERE {where_clause}"
            values = where_values

        # Construct the final query
        query = f"SELECT * FROM {table_name} {where_condition} ORDER BY {order_by} {order} LIMIT ? OFFSET ?"
        values.extend([limit, start])

        # Execute the query
        conn = sqlite3.connect(f"{DB_FOLDER}/{db_name}.db")
        cursor = conn.cursor()
        cursor.execute(query, values)
        rows = cursor.fetchall()
        conn.close()

        # Prepare and return results as a list of dictionaries
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    except sqlite3.Error as e:
        return {"error": str(e)}
