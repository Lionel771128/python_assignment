from fastapi import HTTPException
from financial.database import Database


class FinancialDataDao:
    def __init__(self, db_config):
        self.db_conn = Database(db_config)

    def get_count(self, start_date, end_date, symbol):
        query = """
            SELECT COUNT(*) FROM financial_data
            WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)
        if symbol:
            query += " AND symbol = %s"
            params.append(symbol)

        result = self.db_conn.execute_one(query, tuple(params))
        # result = cursor.fetchone()
        return result[0]

    def get_financial_data(self, start_date, end_date, symbol, limit, offset):
        query = """
                SELECT symbol, date, open_price, close_price, volume
                FROM financial_data
                WHERE 1=1
            """
        params = []
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)
        if symbol:
            query += " AND symbol = %s"
            params.append(symbol)
        query += " LIMIT %s OFFSET %s"
        params.extend((limit, offset))
        return self.db_conn.execute_all(query, tuple(params))

    def get_average_daily_open_price(self, start_date, end_date, symbol):
        avg_open_price = self.__get_average("open_price", start_date, end_date, symbol)
        if avg_open_price is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return round(avg_open_price, 2)

    def get_average_daily_close_price(self, start_date, end_date, symbol):
        avg_open_price = self.__get_average("close_price", start_date, end_date, symbol)
        if avg_open_price is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return round(avg_open_price, 2)

    def get_average_daily_volume(self, start_date, end_date, symbol):
        avg_open_price = self.__get_average("volume", start_date, end_date, symbol)
        if avg_open_price is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return round(avg_open_price)

    # Calculate the average daily open price for the period
    def __get_average(self, get_avg_column_name, start_date, end_date, symbol):
        query = f"SELECT AVG({get_avg_column_name}) FROM financial_data WHERE date >= %s AND date <= %s AND symbol = %s"
        params = (start_date, end_date, symbol)
        open_price_result = self.db_conn.execute_one(query, params)
        if open_price_result[0] is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return open_price_result[0]
