  -- ---- PART 1: Create and Explore the Product Table ----

  DROP TABLE IF EXISTS PRODUCT;

  CREATE TABLE PRODUCT (
      PRO__ID     TEXT PRIMARY KEY,
      PRO__NAME   TEXT NOT NULL,
      PRO_PRICE   INTEGER NOT NULL,
      PRO_COM     TEXT NOT NULL
  );

  -- Insert sample computer store products
  INSERT INTO PRODUCT (PRO_ID, PRO_NAME, PRO_PRICE, PRO_COM) VALUES 
  ('101', 'MOTHER BOARD',     3200, 'TECHPRO'),
  ('102', 'KEY BOARD',         450, 'KEYMAX'),
  ('103', 'ZIP DRIVE',         250, 'DATAFIX'),
  ('104', 'SPEAKER',           550, 'SOUNDCO'),
  ('105', 'MONITOR',          5000, 'VIEWTECH'),
  ('106', 'DVD DRIVE',         900, 'DATAFIX'),
  ('107', 'CD DRIVE',          800, 'DATAFIX'),
  ('108', 'PRINTER',          2600, 'PRINTPLUS'),
  ('109', 'REFILL CARTRIDGE',  350, 'PRINTPLUS'),
  ('110', 'MOUSE',             250, 'KEYMAX');

  -- Display all products
  SELECT * FROM PRODUCT;

  -- ---- PART 2: AND and OR Clause ----

  -- Products priced below 1000 AND made by DATAFIX
  SELECT*
  FROM PRODUCT
  WHERE PRO_PRICE < 1000 AND PRO_COM = 'DATAFIX';

  -- Products made by KEYMAX OR priced above 3000
  SELECT *
  FROM PRODUCT
  WHERE PRO_COM = 'KEYMAX' OR PRO_PRICE > 3000;

  -- Products under 1000 that are either DATAFIX or KEYMAX items
  SELECT *
  FROM PRODUCT
  WHERE PRO_PRICE < 1000
    AND (PRO_COM = 'DATAFIX' OR PRO_COM = 'KEYMAX');

  -- ---- PART 3: LIKE Clause ----

  -- FIND product names that begin with M 
  SELECT * 
  FROM PRODUCT
  WHERE PRO_NAME LIKE 'M%';

  -- FIND product names that end with DRIVE
  SELECT * 
  FROM PRODUCT 
  WHERE PRO_NAME LIKE '%DRIVE';

  -- FIND product names that contain the word PRINT 
  SELECT *
  FROM PRODUCT
  WHERE PRO_NAME LIKE '%PRINT';

  -- ---- PART 4: MIN() and MAX() ----

  -- Find the lowest-priced product
  SELECT PRO_NAME, PRO_PRICE
  FROM PRODUCT
  WHERE PRO_PRICE = (
      SELECT MIN(PRO_PRICE)
      FROM PRODUCT
  );

  -- Find the highest-priced product
  SELECT PRO_NAME, PRO_PRICE
  FROM PRODUCT
  WHERE PRO_PRICE = (
      SELECT MAX(PRO_PRICE)
      FROM PRODUCT
  );

  -- ---- PART 5: UPDATE Query ----

  -- Change the price of the Speaker
  UPDATE PRODUCT
  SET PRO_PRICE = 600
  WHERE PRO_ID = '104';

  -- Check the updated product
  SELECT *
  FROM PRODUCT
  WHERE PRO_ID = '104';

  -- ---- PART 6: DELETE Query ----

  -- Remove the ZIP DRIVE product from the table
  DELETE FROM PRODUCT
  WHERE PRO__ID = '103';
  
  -- Display the remaining products
  SELECT * FROM PRODUCT;