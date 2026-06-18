-- Create the PRODUTS table if it does not exist
CREATE TABLE IF NOT EXISTS PRODUCTS (
    PRODUCT_ID TEXT,
    PRODUCT_NAME TEXT,
    SUPPLIER_ID TEXT,
    CATEGORY_ID TEXT,
    UNIT_TEXT,
    PRICE_REAL
  );

  -- Insert sample data into the PRODUCTS table
  INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, SUPPLIER_ID, CATEGORY_ID, UNIT_TEXT, PRICE_REAL) VALUES
  ('1', 'CHAIS', '1', '1', '10 BOXES*20 BAGS', 18),
  ('2', 'CHANG', '1', '1', '10 BOXES*20 BAGS', 19),
  ('3', 'ANISEED SYRUP', '1', '2', '12-550 ML BOTTLES', 10),
  ('4', 'CHEF ANTON SEASONING', '2', '2', '48-6 OZ JARS', 22),
  ('5', 'CHEF ANTON MIX', '2', '2', '36 BOXES', 21.35);

  -- Query to count the number of products
  SELECT COUNT(PRODUCT_ID) AS Product_Count
  FROM PRODUCTS;

  -- Query to find the average price of products
   SELECT AVG(PRice) AS Average_Count
   FROM PRODUCTS;

   --Query to find the average price of products
   SELECT AVG(PRICE) AS Average_Price
   FROM PRODUCTS;