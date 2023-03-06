CREATE DATABASE if not exists python_assignment;
use python_assignment;
CREATE TABLE if not exists financial_data (
   symbol VARCHAR(50) ,
   date DATE ,
   open_price DECIMAL(10,2),
   close_price DECIMAL(10,2),
   volume INT,
   PRIMARY KEY(symbol, date)
);