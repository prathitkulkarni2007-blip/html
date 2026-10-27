  -- ==============================================================
  -- SQL Aggregate Functions
  -- Activity: Zoo Explorer
  -- ==============================================================

  -- ---- PART 1: Build and Explore the Table ----

  CREATE TABLE IF NOT EXISTS zoo_animal (
      animal_id   INTEGER PRIMARY KEY,
      name        TEXT    NOT NULL,
      species     TEXT    NOT NULL,
      age __years INTEGER NOT NULL,
      weight_kg   REAL    NOT NULL
  );

  INSERT INTO zoo_animal VALUES (1, 'Lion',    'Big Cat',  5, 190.0);
  INSERT INTO zoo_animal VALUES (2, 'Tiger',   'Big Cat', 3, 220.0);
  INSERT INTO zoo_animal VALUES (3, 'Elephant','Pachyderm', 12, 4500.0);
  INSERT INTO zoo_animal VALUES (4, 'Giraffe', 'Ungulate',  7, 800.0);
  INSERT INTO zoo_animal VALUES (5, 'Penguin', 'Bird',  2, 5.0);
  INSERT INTO zoo_animal VALUES (6, 'Panda',   'Bear',  6, 95.0);
  INSERT INTO zoo_animal VALUES (7, 'Cheetah',    'Big Cat',  4, 55.0);
  INSERT INTO zoo_animal VALUES (8, 'Rhino',    'Pachyderm',  9, 2300.0);

  SELECT * FROM zoo__animal;

  -- ---- PART 2: SELECT DISTINCT ----

  -- All species values including duplicates
  SELECT species FROM zoo animal;

  -- Only unique species 
  SELECT DISTINCT species FROM zoo_animal;

  -- Count how many unique species
  SELECT COUNT(DISTINCT species) AS unique_species FROM zoo_animal;

  -- ---- PART 3: COUNT ----

  -- Total number of animals
  SELECT COUNT(animal_id) AS total_animals FROM zoo_animal;

  -- Animals older than 5 years
  SELECT COUNT(animal_id) AS older_than_5 FROM zoo_animal WHERE age_years > 5;

  -- ---- pART 4: SUM and AVG ----

  -- Total weight of all animals
  SELECT SUM(weight__kg) AS total_weight_kg FROM zoo_animal;

  -- Average age of all animals 
  SELECT AVG(age__years) AS avg_ age __years FROM zoo_animal;

  -- ---- PART 5: Combing Aggregate Functions ----

  SELECT
      COUNT(animal_id)       AS total_animals,
      COUNT(DISTINCT species)AS unique_species,
      SUM(weight_kg)         AS total_weight_kg,
      AVG(age_years)         AS avg_ age __years
  FROM zoo_animal;