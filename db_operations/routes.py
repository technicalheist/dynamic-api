from flask import Blueprint, request, jsonify
import sqlite3
from db_operations.utils import (
    execute_query,
    table_exists,
    fetch_data,
    insert_data,
    update_data,
    delete_data,
    parse_where_conditions
)
import  os
op_routes = Blueprint("op_routes", __name__)

# Dynamic route to handle all HTTP methods for a specific table
@op_routes.route("/<db_name>/<table_name>", methods=["GET", "POST", "PUT", "DELETE"])
def table_operations(db_name, table_name):
    """
    Handles GET, POST, PUT, and DELETE requests for a given table in a database.

    GET:
        Retrieves data from the table.
        Parameters:
            limit (int): The number of records to return. Default is 10.
            start (int): The starting record number. Default is 0.
            order (str): The order of the records. Can be "ASC" or "DESC". Default is "ASC".
            orderby (str): The column to order the records by. Default is "id".
            where (dict): Conditions for the WHERE clause. Can contain the following keys:
                column (str): The column name.
                operator (str): The operator to use. Can be "=", "<", ">", "<=", ">=", "<>", "IN", "LIKE", "NOT LIKE".
                value (str): The value to compare with.
        Returns:
            A JSON object with the following keys:
                data (list): The retrieved records.
                status (str): The status of the request. Can be "SUCCESS" or "ERROR".
                message (str): A message describing the status of the request.

    POST:
        Inserts data into the table.
        Parameters:
            data (list): A list of records to insert.
        Returns:
            A JSON object with the following keys:
                status (str): The status of the request. Can be "SUCCESS" or "ERROR".
                message (str): A message describing the status of the request.
                data (list): The inserted records.

    PUT:
        Updates data in the table.
        Parameters:
            update (dict): The values to update. Can contain the following keys:
                column (str): The column name.
                value (str): The new value.
            where (dict): Conditions for the WHERE clause. Can contain the following keys:
                column (str): The column name.
                operator (str): The operator to use. Can be "=", "<", ">", "<=", ">=", "<>", "IN", "LIKE", "NOT LIKE".
                value (str): The value to compare with.
        Returns:
            A JSON object with the following keys:
                status (str): The status of the request. Can be "SUCCESS" or "ERROR".
                message (str): A message describing the status of the request.
                data (list): The updated records.

    DELETE:
        Deletes data from the table.
        Parameters:
            where (dict): Conditions for the WHERE clause. Can contain the following keys:
                column (str): The column name.
                operator (str): The operator to use. Can be "=", "<", ">", "<=", ">=", "<>", "IN", "LIKE", "NOT LIKE".
                value (str): The value to compare with.
        Returns:
            A JSON object with the following keys:
                status (str): The status of the request. Can be "SUCCESS" or "ERROR".
                message (str): A message describing the status of the request.
                data (list): The deleted records.
    """
    if not table_exists(db_name, table_name):
        return jsonify({"status": "ERROR", "message": f"Table {table_name} does not exist in database {db_name}"}), 400

    if request.method == "GET":
        try:
            limit = int(request.args.get("limit", 10))
            start = int(request.args.get("start", 0))
            order = request.args.get("order", "ASC").upper()
            order_by = request.args.get("orderby", "id")
            if order not in ["ASC", "DESC"]:
                return jsonify({"status": "ERROR", "message": "Invalid order parameter"}), 400
            where_clause, where_values = parse_where_conditions(request.args)
            data = fetch_data(db_name, table_name, limit, start, order_by, order, where_clause, where_values)
            return jsonify({"data": data, "status": "SUCCESS", "message": "Data Fetched Successfully"}), 200
        except Exception as e:
            return jsonify({"status": "ERROR", "message": str(e)}), 400

    if request.method == "POST":
        try:
            data = request.get_json().get("data")
            if not data:
                return jsonify({"status": "ERROR", "message": "Data is required for insertion"}), 400

            result = insert_data(db_name, table_name, data)
            
            # Check if result contains an error message
            if "error" in result:
                return jsonify({"status": "ERROR", "message": result["error"]}), 400
            
            return jsonify({
                "status": "SUCCESS", 
                "message": "Data Inserted Successfully", 
                "data": result
            }), 200
            
        except Exception as e:
            return jsonify({"status": "ERROR", "message": f"An error occurred: {str(e)}"}), 400

    if request.method == "PUT":
        try:
            update_values = request.get_json().get("update")
            where_conditions = request.get_json().get("where")
            if not update_values or not where_conditions:
                return jsonify({"status": "ERROR", "message": "Both 'update' and 'where' conditions are required"}), 400
            result = update_data(db_name, table_name, update_values, where_conditions)
            return jsonify({"status": "SUCCESS", "message": "Data Updated Successfully", "data": result}), 200
        except Exception as e:
            return jsonify({"status": "ERROR", "message": str(e)}), 400

    if request.method == "DELETE":
        try:
            where_conditions = request.get_json().get("where")
            if not where_conditions:
                return jsonify({"status": "ERROR", "message": "'where' conditions are required for deletion"}), 400
            result = delete_data(db_name, table_name, where_conditions)
            return jsonify({"status": "SUCCESS", "message": "Data Deleted Successfully", "data": result}), 200
        except Exception as e:
            return jsonify({"status": "ERROR", "message": str(e)}), 400

@op_routes.route('/sql', methods=['POST'])
def execute_sql():
    """
    Execute a raw SQL query against a specific database

    This endpoint expects a JSON payload with two keys: 'query' and 'db_name'.
    The 'query' key should contain the raw SQL query to execute, and the 'db_name'
    key should contain the name of the database to execute the query against.

    If the query is a SELECT query, the response will contain the results of the query
    as a list of dictionaries, where each dictionary represents a row in the result set.
    If the query is not a SELECT query, the response will contain a success message
    indicating that the query was executed successfully.

    If an error occurs while executing the query, the response will contain an error
    message with details about the error.
    """
    try:
        # Get the raw SQL query from the request body
        data = request.get_json()
        sql_query = data.get("query")
        db_name = data.get("db_name")
        
        if not sql_query or not db_name:
            return jsonify({"status" : "ERROR", "message": "Missing SQL query or database name"}), 400

        # Connect to the database
        conn = sqlite3.connect(f"databases/{db_name}.db")
        cursor = conn.cursor()
        
        # Execute the SQL query
        cursor.execute(sql_query)
        
        # If it's a SELECT query, fetch the data
        if sql_query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
        else:
            conn.commit()
            result = {"status" : "ERROR", "message": "Query executed successfully"}
        
        # Close the connection
        conn.close()
        
        # Return the result
        return jsonify({"status" : "SUCCESS", "data" : result})

    except sqlite3.Error as e:
        return jsonify({"status" : "ERROR", "message": str(e)}), 400
    
    
@op_routes.route("/<db_name>/<table_name>/<id>", methods=['GET'])
def get_by_id(db_name, table_name, id):
    """
    Retrieve a record by its ID from a specific table in a database.

    This endpoint fetches a single record from the specified table in the given database
    using the record's ID. The ID is passed as a part of the URL.

    Parameters:
        db_name (str): The name of the database.
        table_name (str): The name of the table from which to retrieve the record.
        id (str): The ID of the record to retrieve.

    Returns:
        JSON response containing:
        - status (str): "SUCCESS" if the record is found, "ERROR" otherwise.
        - data (dict): The record data if found, or an error message if not.

    Errors:
        - Returns an error if the database name is missing.
        - Returns an error if there is an issue with the database operation.
    """
    try:
        if not db_name:
            return jsonify({"status" : "ERROR", "message": "Missing database name"}), 400

        # Connect to the database
        conn = sqlite3.connect(f"databases/{db_name}.db")
        cursor = conn.cursor()
        
        # Execute the SQL query
        sql_query = f"SELECT * FROM {table_name} WHERE id = ?"
        cursor.execute(sql_query, (id,))
        
        # Fetch the data
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            result = dict(zip(columns, row))
        else:
            result = {"status": "ERROR", "message": "Data Not Available"}
        
        # Close the connection
        conn.close()
        
        # Return the result
        return jsonify({ "status" : "SUCCESS", "data" : result})

    except sqlite3.Error as e:
        return jsonify({"status" : "ERROR", "message": str(e)}), 400


@op_routes.route("/<db_name>/<table_name>/<id>", methods=["DELETE"])
def delete_by_id(db_name, table_name, id):
    """
    Deletes a record from the specified table in the specified database by its ID.

    Parameters:
        - db_name (str): The name of the database.
        - table_name (str): The name of the table.
        - id (int): The ID of the record to delete.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the record is deleted, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.

    Errors:
        - Returns an error if the database name is missing.
        - Returns an error if the record is not found.
        - Returns an error if there is an issue with the database operation.
    """
    try:
        db_path = os.path.join("databases", f"{db_name}.db")
        if not os.path.exists(db_path):
            return jsonify({"status": "error", "message": f"Database {db_name} does not exist"}), 404

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = f"DELETE FROM {table_name} WHERE id = ?"
        cursor.execute(query, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Record not found"}), 404

        conn.close()
        return jsonify({"status": "SUCCESS", "message": "Record deleted successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@op_routes.route("/<db_name>/<table_name>/<id>", methods=["PUT"])
def update_by_id(db_name, table_name, id):
    """
    Updates a record in a table by ID.

    Parameters:
        - db_name (str): The name of the database.
        - table_name (str): The name of the table.
        - id (int): The ID of the record to update.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the record is updated, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.
            - data (dict): The updated data for the record.

    Errors:
        - Returns an error if the database name is missing.
        - Returns an error if the record is not found.
        - Returns an error if there is an issue with the database operation.
    """
    try:
        # Get the updated data from the payload
        data = request.get_json()

        # Check if the database exists
        db_path = os.path.join("databases", f"{db_name}.db")
        if not os.path.exists(db_path):
            return jsonify({"status": "ERROR", "message": f"Database {db_name} does not exist"}), 404

        # Prepare the SET part of the SQL query
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values())

        # Prepare the full query
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        
        # Execute the query
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, values + (id,))
        conn.commit()

        # Check if any rows were updated
        if cursor.rowcount == 0:
            return jsonify({"status": "ERROR", "message": "Record not found or no changes made"}), 404
        
        conn.close()

        return jsonify({
            "status": "SUCCESS", 
            "message": "Record updated successfully", 
            "data": data
        }), 200

    except sqlite3.Error as e:
        return jsonify({"status": "ERROR", "message": f"Database error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"An error occurred: {str(e)}"}), 400
