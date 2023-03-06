import mysql.connector


class Database:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
            # auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def execute_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def execute_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
        # self.connection.commit()

    def close(self):
        self.connection.close()

