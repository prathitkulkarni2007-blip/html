 CREATE TABLE Persons (
     PersonID int,
     LastName varchar(255),
     FirstName vachar(255),
     Address vachar(255),
     City varchar(255)
 );
  CREATE TABLE Persons (
     PersonID int,
     LastName varchar(255),
     FirstName varchar(255),
     Address varchar(255),
     City varchar(255)
  );
  INSERT INTO table_name (column1, column2, column3, ...)
  VALUES (value1, value2, value3, ...);
  INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
  VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');
  DROP TABLE table_name;
  DROP TABLE Shippers;
  SELECT column1, column2, ...
  FROM table_name;
  SELECT * FROM table_name;
  SELECT CustomerName, City FROM Customers;
  SELECT * FROM Customers;
  SELECT column1, column2, ...
  FROM table_name
  WHERE condition;
  SELECT * FROM Customers
  WHERE Country='Mexico';
  -- 1) Create a table for Salesman details:
  -- a) Use `CREATE TABLE IF NOT EXISTS` to avoid errors if the table already exists.
  -- b) Add columns for id, name, city, and commission.
  -- c) Set the id column as `CREATE TABLE IF NOT EXISTS` to avoid errors if the table already exists.

  -- 2) Insert sample records into the Salesman table:
  --    a) Use a single `INSERT INTO ... VALUES` with multiple rows.

  -- 3) Display all records from the Salesman table:
  --  a) Use `SELECT * FROM Salesman;`

  -- 4) Create a table for Orders details:
  --    a) Use `CREATE TABLE IF NOT EXISTS`.
  --    b) Add columns for order number, purchase amount, order date, customer id, and salesman id.
  --    c) Set the order number as `PRIMARY KEY`.

  -- 5) Insert sample records into the Orders table:
  --    a) Use `INSERT INTO ... VALUES` with multiple rows.

  -- 6) Display all records from the Orders table:
  --    a) Use `SELECT * FROM Orders;`

  -- 7) Select specific columns from Salesman table:
  --    a) Use `SELECT name, Comission FROM Salesman;` to show name and commission.