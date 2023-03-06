# python_assignment


## Description


This project provides a RESTful API to retrieve financial data from AlphaVantage. The API supports various endpoints to retrieve stock prices, exchange rates, and technical indicators for a given symbol and time period.

## Tech Stack


The project uses the following technologies:

- Python 3.11.2
- Docker 20.10.8
- FastAPI 2.1.1 : A modern, fast (high-performance), web framework for building APIs
- Uvicorn 0.20.0 : An ASGI server, for production.
- MySQL 8.0 : I am more familiar with MySQL due to my current job position, so I choose it.
- mysql-connector-python: MySQL driver written in Python
- typing_extensions: To implement the optional parameters when use FastAPI  

## How to Run


To run the project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/username/financial-api.git
```

2. Install the required packages:

```
cd python_assignment
pip install -r requirements.txt
```

3. Run Server:

```
docker compose up -d
```

4. Initial the database <br>
   Before you initial the database, please edit the db host in config.ini.
   The default value is container name, so when initial the database, 
   change it to the database server's IP.
```
python get_raw_data.py
```

## Maintaining the API Key

To stored API KEY securely, I don't set the API KEY in the config.ini. <br>
And to maintain easily , you can store your API KEY file at every folder you want, <br>
when you want to change the key, just edit the config.ini and do all following step at **Maintain the API KEY**

### Setting API KEY before run service

Before you run server, please set the API Key's file path in Config.ini.


### Maintain the API KEY

1. Edit API Key's file path in Config.ini.

2. docker cp to the api container
```
docker cp [API KEY file path] api:[API KEY location]
```

3. restart service

```
docker restart api
```