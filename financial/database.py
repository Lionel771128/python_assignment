import mysql.connector

"""
A class representing a database connection.

Attributes:
    connection: A connection to the MySQL database.
    cursor: A cursor for executing MySQL queries.
"""
class Database:

    """
    Initializes a new instance of the Database class.

    Args:
        db_config: A dictionary containing the database configuration.
    """
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
            # auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    """
    Executes a single MySQL query and returns the first result.

    Args:
        query: The MySQL query to execute.
        params: A tuple containing any parameters for the query.

    Returns:
        The first result of the query, or None if no results were found.
    """
    def execute_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    """
    Executes a MySQL query and returns all results.

    Args:
        query: The MySQL query to execute.
        params: A tuple containing any parameters for the query.

    Returns:
        A list of tuples containing the results of the query.
    """
    def execute_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
        # self.connection.commit()

    """
    Closes the database connection.
    """
    def close(self):
        self.connection.close()

