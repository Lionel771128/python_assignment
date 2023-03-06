from datetime import datetime, timedelta
import mysql.connector
import requests
import utils

"""
Create a MySQL connection object using the provided configuration.

Args:
    db_config: A dictionary containing the MySQL database configuration parameters.
    choose_db: A boolean indicating whether to connect to a specific database. Default is True.

Returns:
    A MySQL connection object.
"""
def create_mysql_connection(db_config, choose_db=True):
    conn = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"] if choose_db else None
    )
    return conn



"""
Retrieve financial data from the Alpha Vantage API.

Args:
    alpha_vantage_api_config: A dictionary containing the configuration parameters for the Alpha Vantage API.

Returns:
    A list of financial data dictionaries, with one dictionary per day per symbol.
"""
def get_raw_data(alpha_vantage_api_config):
    financial_data = []
    days = 14
    today = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    api_endpoint = f"{alpha_vantage_api_config['base_url']}/{alpha_vantage_api_config['action']}"
    symbols = alpha_vantage_api_config["symbols"].split(",")
    for symbol in symbols:
        payload = {
            "function": alpha_vantage_api_config["function"],
            "symbol": symbol,
            "outputsize": alpha_vantage_api_config["output_size"],
            "apikey": alpha_vantage_api_config["api_key"]
        }

        response = requests.get(api_endpoint, params=payload)
        if response.status_code == 200:
            data = response.json()
            for date, values in data['Time Series (Daily)'].items():
                if not (date >= start_date and date <= today):
                    break
                financial_data.append({
                    "symbol": symbol,
                    "date": date,
                    "open_price": values['1. open'],
                    "close_price": values['4. close'],
                    "volume": values['6. volume']
                })
    return financial_data



"""
Insert financial data into the MySQL database.

Args:
    db_config: A dictionary containing the MySQL database configuration parameters.
    financial_data: A list of financial data dictionaries, with one dictionary per day per symbol.

Returns:
    None.
"""
def insert_to_db(db_config, financial_data):
    db_conn = create_mysql_connection(db_config, choose_db=True)
    # Insert records into the financial_data table in the MySQL database
    with db_conn.cursor() as cursor:
        for data in financial_data:
            cursor.execute("INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE open_price = VALUES(open_price), close_price = VALUES(close_price), volume = VALUES(volume)", (data['symbol'], data['date'], data['open_price'], data['close_price'], data['volume']))
        db_conn.commit()
        print(cursor.rowcount, "records inserted into the financial_data table")


"""
Create a MySQL database by executing a Data Definition Language (DDL) script.

Args:
    db_config (dict): A dictionary containing the database configuration parameters.
"""
def create_db_by_ddl(db_config):
    db_conn = create_mysql_connection(db_config, choose_db=False)
    cursor = db_conn.cursor()
    with open(db_config["ddl_file_path"], "r") as script:
        # Read the contents of the script file
        sql = script.read()
        # Split the SQL statements by semicolon (;)
        statements = sql.split(";")
        # Execute each SQL statement
        for statement in statements:
            cursor.execute(statement)
    db_conn.commit()
    db_conn.close()


def initial_db():
    db_config = utils.get_config("config.ini", "db")
    alpha_vantage_api_config = utils.get_config("config.ini", "alpha_vantage_api")
    create_db_by_ddl(db_config)
    financial_data = get_raw_data(alpha_vantage_api_config)
    insert_to_db(db_config, financial_data)


initial_db()
