CREATE TABLE IF NOT EXISTS Saleman(
Salesman_id TEXT PRIMARY KEY,
name TEXT,
city TEXT,
Comission TEXT
);
 INSERT INTO Salesman(Salesman_id,name,city,Comission)
 VALUES
   ("5001", "James Hoog", "New York", "0.15"),
   ("5002", "Nail Knite", "Paris", "0.13"),
   ("5005", "Pit Alex", "London", "0.11"),
   ("5006", "Mc Lyon", "Paris", "0.14")
   ("5007", "Paul Adam", "Rome","0.13"),
   ("5003", "Lauson Hen", "San Jose","0.12");

 CREATE TABLE IF NOT EXISTS Customer(
    customer_id TEXT,
    cust_name TEXT PRIMARY KEY,
    city TEXT,
    grade TEXT,
    Salesman_id TEXT
  );
  INSERT INTO Customer(customer_id,cust_name,city,grade,Saleman_id)
  VALUES
    ("3002","nick rimando","new york","100","5001"),
    ("3007","brad davis","new york","200","5001"),
    ("3005","graham zusi","california","200","5002"),
    ("3008","julian green","london","300","5002"),
    ("3004","fabian johnson","paris","300","5006),
    ("3009","geoff cameron","berlin","100","5003"),
    ("3003","jozy altidor","moscow","200","5007"),
    ("3001", "brad guzan","london","","5005");

   CREATE TABLE IF NOT EXISTS Orders(
     ord_no TEXT PRIMARY KEY,
     purch_amt TEXT,
     ord_date TEXT,
     customer_id TEXT,
     Salesman_id TEXT
  );
  INSERT INTO Orders(ord no,purch amt,ord date,customer id,Saleman id)
  VALUES
    ("70001","150.5","2012-10-05","3005","5002")
    ("70009","270.65","2012-09-10","3001","5001"),
    ("70002","65.26","2012-10-05","3002","5003"),
    ("70004","110.5","2012-08-17","3009","5007"),
    ("70007","948.5","2012-09-10","3005","5005"),
    ("70005","2400.6","2012-07-27","3007","5006");

 -- Queries 

 -- Matching customers and salesman by city
 SELECT customer.cust_name, salesman.name, salesman.city
 FROM Customer
 JOIN Salesman ON Customer.city = Salesman.city;

 -- Linking customers to their salesmen
 SELECT Customer.cust_name, Salesman.name
 FROM Customer
 JOIN Salesman ON Customer.Salesman_id = Salesman.Saleman_id;

 -- Fetching orders where customer's city does not match salesman's city
 SELECT Orders.ord_no, Customer.cust_name, Orders.customer_id, Orders.Salesman_id
 FROM Orders
 JOIN Customer ON Orders.customer_id = Customer.customer_id
 JOIN Salesman ON Orders.Salesman_id = Salesman.Salesman_id
 WHERE Customer.city <> Salesman.city;

 -- Fetching all orders with customer names
 SELECT Orders.ord_no, Customer.cust_name
 FROM Orders
 JOIN Customer ON Orders.customer_id = Customer.customer_id;

 -- Customers with grades
 SELECT Customer.cust_name AS "Customer", Customer.grade AS "Grade"
 FROM Orders
 JOIN Salesman ON Orders.Salesman_id = Salesman.Salesman_id
 JOIN Customer ON Orders.customer_id = Customer.customer_id
 WHERE Customer.grade IS NOT NULL;

 -- Customers with salesmen where commission is between 0.12 and 0.14
 SELECT Customer.cust_name AS "Customer",
 Customer.city AS "City",
 Salesman.name AS "Salesman",
 Salesman.commission
 FROM Customer
 JOIN Salesman ON Customer.Salesman_id = Salesman.Salesman_id
 WHERE Salesman.commission BETWEEN 0.12 AND 0.14;

 -- Calculating commissions for orders where customer grade is 200 or more
 SELECT Orders.ord_no, Customer.cust_name, Salesman.commission AS "Commission%",
 Orders.purch_amt * Salesman.commission AS "Commission"
 FROM Orders
 JOIN Salesman ON Orders.Salesman_id = Salesman.Salesman_id
 JOIN Customer ON Orders.customer_id = Customer.customer_id
 WHERE Customer.grade >= 200;

 -- Orders on a specific date 
 SELECT *
 FROM Customer
 JOIN Orders ON Customer.customer_id = Orders.customer_id
 WHERE Orders.ord_date = '2012-10-05';,