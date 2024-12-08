from flask import Blueprint, request, jsonify
from schema.db_utils import (
    create_db,
    delete_db,
    create_table,
    alter_table_add_column,
    alter_table_remove_column,
    truncate_table,
    delete_table,
    list_databases,
    list_tables,
    table_details, 
    rename_table,
    rename_column
)

db_routes = Blueprint("db_routes", __name__)

@db_routes.route("/", methods=["POST"])
def route_create_db():
    """
    Creates a new database in the system.

    Parameters:
        - db_name (str): The name of the database to be created.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the database is created, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.

    Errors:
        - Returns an error if the database name is missing.
        - Returns an error if there is an issue with the database operation.
    """
    data = request.get_json()
    db_name = data.get("name")
    if not db_name:
        return jsonify({"error": "name is required"}), 400
    return jsonify(create_db(db_name))

@db_routes.route("/", methods=["GET"])
def route_list_databases():
    """
    Lists all databases available.

    This endpoint handles GET requests to retrieve a list of all
    databases in the system.

    Returns:
        JSON response containing:
            - databases (list): A list of database names.
    """
    return jsonify(list_databases())

@db_routes.route("/<db_name>", methods=["DELETE"])
def route_delete_db(db_name):
    """
    Deletes a database from the system.

    Parameters:
        - db_name (str): The name of the database to be deleted.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the database is deleted, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.

    Errors:
        - Returns an error if the database name is missing.
        - Returns an error if there is an issue with the database operation.
    """
    data = request.get_json()
    if not db_name:
        return jsonify({"error": "db_name is required"}), 400
    return jsonify(delete_db(db_name))

@db_routes.route("/<db_name>", methods=["GET"])
def route_list_tables(db_name):
    """
    Lists all tables within a specified database.

    This endpoint handles GET requests to retrieve a list of all
    tables in the specified database.

    Parameters:
        db_name (str): The name of the database for which to list tables.

    Returns:
        JSON response containing:
            - tables (list): A list of table names within the specified database.
            - error (str, optional): An error message if the database does not exist.
    """
    return jsonify(list_tables(db_name))

@db_routes.route("/<db_name>/<table_name>", methods=["POST"])
def route_create_table(db_name, table_name):
    """
    Creates a new table in the specified database.

    This endpoint expects a JSON payload with the following keys:
        - db_name (str): The name of the database where the table will be created.
        - table_name (str): The name of the table to create.
        - columns (list): A list of dictionaries, each representing a column with keys:
            - name (str): The column name.
            - type (str): The data type of the column.
            - primary_key (bool, optional): Whether the column is a primary key.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the table is created, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.

    Errors:
        - Returns an error if any of db_name, table_name, or columns is missing.
        - Returns an error if there is an issue with the table creation.
    """
    data = request.get_json()
    columns = data.get("columns")
    if not db_name or not table_name or not columns:
        return jsonify({"error": "db_name, table_name, and columns are required"}), 400
    return jsonify(create_table(db_name, table_name, columns))

@db_routes.route("/<db_name>/<table_name>", methods=["GET"])
def route_table_details(db_name, table_name):
    """
    Retrieves table details for a given database and table.

    This endpoint handles GET requests to retrieve a dictionary containing
    the following information about the specified table:
        - columns (list): A list of dictionaries, each containing the column's
            name and data type.

    Parameters:
        db_name (str): The name of the database containing the table.
        table_name (str): The name of the table for which to retrieve details.

    Returns:
        JSON response containing:
            - columns (list): A list of column dictionaries.

    Errors:
        - Returns an error if the database or table does not exist.
    """
    return jsonify(table_details(db_name, table_name))

@db_routes.route("/<db_name>/<table_name>", methods=["DELETE"])
def route_delete_table(db_name, table_name):
    """
    Deletes a specified table from a database.

    This endpoint expects a JSON payload with the following keys:
        - db_name (str): The name of the database containing the table.
        - table_name (str): The name of the table to delete.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the table is deleted successfully, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.

    Errors:
        - Returns an error if db_name or table_name is missing.
        - Returns an error if there is an issue with deleting the table.
    """
    if not db_name or not table_name:
        return jsonify({"error": "db_name and table_name are required"}), 400
    return jsonify(delete_table(db_name, table_name))

@db_routes.route("/<db_name>/<table_name>", methods=["PUT"])
def route_alter_table(db_name, table_name):
    """
    Alters the structure of a specified table in a database by adding or removing columns.

    This endpoint expects a JSON payload with the following keys:
        - db_name (str): The name of the database containing the table.
        - table_name (str): The name of the table to alter.
        - add_column (list or dict, optional): A list of dictionaries or a single dictionary specifying columns to add.
            Each dictionary should have:
            - name (str): The column name.
            - type (str): The data type of the column.
        - remove_column (list or str, optional): A list of column names or a single column name to remove from the table.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the table is altered successfully, "ERROR" otherwise.
            - message (str): A message describing the result of the operation for each column addition or removal.

    Errors:
        - Returns an error if db_name or table_name is missing.
        - Returns an error if there is an issue with adding or removing columns.
    """
    data = request.get_json()
    add_columns = data.get("add_column")  # List of columns to add
    remove_columns = data.get("remove_column")  # List of columns to remove

    if not db_name or not table_name:
        return jsonify({"error": "db_name and table_name are required"}), 400

    result = {}

    # Handle adding columns
    if add_columns:
        if isinstance(add_columns, list):
            for col in add_columns:
                result[f"add_column_{col['name']}"] = alter_table_add_column(db_name, table_name, col)
        else:
            result["add_column"] = alter_table_add_column(db_name, table_name, add_columns)

    # Handle removing columns
    if remove_columns:
        if isinstance(remove_columns, list):
            for col in remove_columns:
                result[f"remove_column_{col}"] = alter_table_remove_column(db_name, table_name, col)
        else:
            result["remove_column"] = alter_table_remove_column(db_name, table_name, remove_columns)

    return jsonify(result)

@db_routes.route("/<db_name>/<table_name>/truncate", methods=["POST"])
def route_truncate_table(db_name, table_name):
    """
    Truncates a specified table in a database, removing all rows and resetting the auto-incrementing ID.

    This endpoint expects a JSON payload with the following keys:
        - db_name (str): The name of the database containing the table.
        - table_name (str): The name of the table to truncate.

    Returns:
        - JSON response containing:
            - status (str): "SUCCESS" if the table is truncated successfully, "ERROR" otherwise.
            - message (str): A message describing the result of the operation.

    Errors:
        - Returns an error if db_name or table_name is missing.
        - Returns an error if there is an issue with truncating the table.
    """
    data = request.get_json()
    if not db_name or not table_name:
        return jsonify({"error": "db_name and table_name are required"}), 400
    return jsonify(truncate_table(db_name, table_name))

@db_routes.route("/<db_name>/<table_name>/rename", methods=["POST"])
def route_rename_table(db_name, table_name):
    """
    Renames a table in a database.

    This endpoint expects a JSON payload with the following keys:
        - db_name (str): The name of the database containing the table.
        - old_table_name (str): The current name of the table.
        - new_table_name (str): The new name for the table.

    Returns:
        - JSON response containing:
            - message (str): A message describing the result of the operation.
            - error (str, optional): An error message if the operation fails.

    Errors:
        - Returns an error if db_name, old_table_name, or new_table_name is missing.
        - Returns an error if there is an issue with renaming the table.
    """
    data = request.get_json()
    new_table_name = data.get("new_table_name")

    if not db_name or not table_name or not new_table_name:
        return jsonify({"error": "db_name, table_name, and new_table_name are required"}), 400

    result = rename_table(db_name, table_name, new_table_name)
    return jsonify(result), 200 if "message" in result else 500

@db_routes.route("/<db_name>/<table_name>/rename_column", methods=["POST"])
def route_rename_column(db_name, table_name):
    """
    Renames a column in a specified table within a database.

    This endpoint expects a JSON payload with the following keys:
        - db_name (str): The name of the database containing the table.
        - table_name (str): The name of the table containing the column.
        - old_column_name (str): The current name of the column.
        - new_column_name (str): The new name for the column.

    Returns:
        - JSON response containing:
            - message (str): A message describing the result of the operation.
            - error (str, optional): An error message if the operation fails.

    Errors:
        - Returns an error if db_name, table_name, old_column_name, or new_column_name is missing.
        - Returns an error if there is an issue with renaming the column.
    """
    data = request.get_json()
    old_column_name = data.get("old_column_name")
    new_column_name = data.get("new_column_name")

    if not db_name or not table_name or not old_column_name or not new_column_name:
        return jsonify({"error": "db_name, table_name, old_column_name, and new_column_name are required"}), 400

    result = rename_column(db_name, table_name, old_column_name, new_column_name)
    return jsonify(result), 200 if "message" in result else 500

