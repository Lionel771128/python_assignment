from fastapi import FastAPI, HTTPException
from typing import Optional
import utils
from financial.financial_data_dao import FinancialDataDao

app = FastAPI()

# Load database configuration from config.ini file
db_cfg = utils.get_config("config.ini", "db")

# Define default limit and error message
DEFAULT_LIMIT = 5
ERROR_MSG = {'error': ''}


"""
Helper function to format result set

Args:
- rs: ResultSet object containing financial data

Returns:
- A list of dictionaries representing formatted financial data
"""
def format_result_set(rs):
    results = []
    for row in rs:
        result = {
            'symbol': row[0],
            'date': row[1].strftime('%Y-%m-%d'),
            'open_price': str(row[2]),
            'close_price': str(row[3]),
            'volume': str(row[4])
        }
        results.append(result)
    return results



"""
API endpoint to retrieve financial data

Args:
- start_date: optional string representing the start date of the financial data
- end_date: optional string representing the end date of the financial data
- symbol: optional string representing the stock symbol of the financial data
- limit: optional integer representing the maximum number of financial data to retrieve per page (default is 5)
- page: optional integer representing the page number of the financial data to retrieve (default is 1)

Returns:
- A dictionary containing the financial data, pagination information, and error message (if any)
"""
# API endpoint to retrieve financial data
@app.get('/api/financial_data')
def get_financial_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    symbol: Optional[str] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    page: Optional[int] = 1
):
    try:
        financial_data_dao = FinancialDataDao(db_cfg)

        # Calculate offset based on page number and limit
        offset = (page - 1) * limit

        # Get count of all records
        count = financial_data_dao.get_count(start_date, end_date, symbol)

        # Calculate total number of pages
        pages = (count + limit - 1) // limit

        # Get financial data
        financial_data = financial_data_dao.get_financial_data(start_date, end_date, symbol, limit, offset)
        results = format_result_set(financial_data)

        # Build pagination dictionary
        pagination = {
            'count': count,
            'page': page,
            'limit': limit,
            'pages': pages
        }
    except Exception as e:
        # Raise HTTPException if there's an error retrieving financial data
        raise HTTPException(status_code=500, detail=f"status_cod:500, info: {e.msg}")

    return {
        'data': results,
        'pagination': pagination,
        'info': ERROR_MSG
    }


"""
API endpoint to retrieve statistics based on financial data

Args:
- start_date: string representing the start date of the financial data
- end_date: string representing the end date of the financial data
- symbol: string representing the stock symbol of the financial data

Returns:
- A dictionary containing the statistics data and error message (if any)
"""
@app.get("/api/statistics")
async def get_statistics(start_date: str, end_date: str, symbol: str):

    try:
        # get the average values
        financial_data_dao = FinancialDataDao(db_cfg)
        average_daily_open_price = financial_data_dao.get_average_daily_open_price(start_date, end_date, symbol)
        average_daily_close_price = financial_data_dao.get_average_daily_close_price(start_date, end_date, symbol)
        average_daily_volume = financial_data_dao.get_average_daily_volume(start_date, end_date, symbol)
        statistics = {
            "start_date": start_date,
            "end_date": end_date,
            "symbol": symbol,
            "average_daily_open_price": average_daily_open_price,
            "average_daily_close_price": average_daily_close_price,
            "average_daily_volume": average_daily_volume
        }
    except Exception as e:
        # Raise HTTPException if there's an error retrieving financial data
        raise HTTPException(status_code=500, detail=f"status_cod:500, info: {e.msg}")

    return {"data": statistics, "info": {"error": ""}}
