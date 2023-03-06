# python_assignment

---

## Description

---

This project provides a RESTful API to retrieve financial data from AlphaVantage. The API supports various endpoints to retrieve stock prices, exchange rates, and technical indicators for a given symbol and time period.

## Tech Stack

---

The project uses the following technologies:

- Python 3.11.2
- Docker 20.10.8
- FastAPI 2.1.1 : A modern, fast (high-performance), web framework for building APIs
- Uvicorn 0.20.0 : An ASGI server, for production.
- MySQL 8.0 : I am more familiar with MySQL due to my current job position, so I choose it.
- mysql-connector-python: MySQL driver written in Python
- typing_extensions: To implement the optional parameters when use FastAPI  

## How to Run

---

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

3.Run Server:

```
docker compose up -d
```

4. Initial the database
p.s. Before you initial the database, please edit the db host in config.ini.
     The default value is container name, so when initial the database, 
     change it to the database server's IP.
```
python get_raw_data.py
```

## Maintaining the API Key

To retrieve financial data from AlphaVantage, you need an API key. To maintain the API key in both local development and production environments, follow these steps:

1. Create an account on the AlphaVantage website to obtain an API key.

2. In your local development environment, set the `ALPHA_VANTAGE_API_KEY` environment variable to the API key. You can set this variable in a shell script or in your IDE's configuration.

3. In the production environment, you should store the API key as a secret or environment variable in your deployment tool (e.g. Kubernetes, Docker Swarm, AWS ECS). Avoid storing the API key in your code or in plain text files.

4. If you need to rotate the API key, update the environment variable or secret in all relevant places. Make sure to update any documentation or scripts that reference the API key as well.