 # ====================================================
 # Query with Subquery 
 # Activity: Science Experiment Explorer
 # ====================================================
 
 import sqlite3
 import pandas as pd 

 # ---- PART 1: Build and Explore the Tables ----

 conn = sqlite3.connect(':memory:')
 
 conn.execute(
     "CREATE TABLE experiment ("
     "experiment_id INTEGER PRIMARY KEY, "
     "experiment_name TEXT NOT NULL, "
     "subject TEXT NOT NULL, "
     "duration_mins INTEGER NOT NULL)"
  )

  conn.execute(
      "CREATE TABLE material ("
      "material_id INTEGER PRIMARY KEY, "
      "experiment_id INTEGER NOT NULL, "
      "item TEXT NOT NULL, "
      "quanitity _g INTEGER NOT NULL)"
 )

 conn.executemany("INSERT INTO experiment VALUES (?, ?, ?, ?)", [
     (1, 'Volcano Reaction', 'Chemistry', 20),
     (2, 'Plant Growth Test', 'Biology', 15),
     (3, 'Magnet Strength Test', 'Physics', 45),
     (4, 'Light Reflection', 'Physics', 30),
     (5, 'Water Filtration', 'Earth Science', 10),


 conn.executemany("INSERT INTO material VALUES (?, ?, ?, ?)", [
     (1, 1, 'Barking Soda', 100),
     (2, 1, 'Vinegar',  150),
     (3, 2, 'Soil', 250),
     (4, 2, 'Seeds', 20),
     (5, 3, 'Bar Magnet', 80),
     (6, 4, 'Mirror', 120),
     (7, 5,  'Sand', 150),
     (8, 5,  'Filter Paper', 10),
 ])

 conn.commit()

 print("Experiment table:")
 print(pd.read__sql("SELECT * FROM experiment", conn))
 print()

 print("Material table:")
 print(pd.read_sql("SELECT * FROM material", conn))
 print()


 # ---- PART 2: Alias for Columns ----

 col__alias = pd.read_sql(
      "SELECT experiment_name AS activity, subject AS topic, "
      "duration_mins AS time "
      "FROM experiment",
      conn 
 )

 print("Column aliases -- activity, topic, time:")
 print(col_alias)
 print()


 # ---- PART 3: Alias for Tables ----

 tbl__alias = pd.read_sql(
     "SELECT e.experient_name AS activity, m.item, "
     "m.quantity__g AS grams "
     "FROM experiment  AS e "
     "INNER JOIN material AS m "
     "ON e.experient_id = m.experiment_id",
     conn 
 )

 print("Table aliases -- e for experiment, m for material:")
 print(tbl_alias)
 print()


 # ---- PART 4: Subquery with IN ----

 large_materials = pd.read_sql(
     "SELECT experiment_name AS activity, subject AS topic "
     "FROM experiment "
     "WHERE experiment_id IN ("
     "SELECT experiment_id FROM material WHERE quantity _g > 100"
     ")",
     conn 
 ) 

 print("Subquery with IN -- experiments with a material over 100g:")
 print(large_materials)
 print()


 # ---- PART 5: Subquery with = ----

 quickest = pd.read_sql(
     "SELECT experiment_name AS activity, duration_mins AS time "
     "FROM experiment "
     "WHERE duration_mins = (SELECT MIN(duration_mins) FROM experiment)",
     conn 
 ) 

 print("Subquery with = -- the quickest experiment:")
 print(quickest)

 conn.close()