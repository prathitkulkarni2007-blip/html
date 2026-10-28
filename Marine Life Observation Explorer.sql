 -- ==========================================================
 -- SOL Aggregate Functions
 -- Activity: Marine Life Observation Explorer
 -- ==========================================================

 -- ---- PART 1: Build and Explore the Table ----

 CREATE TABLE IF NOT EXISTS marine_observation (
     observation_id       INTEGER PRIMARY KEY,
     animal_name          TEXT    NOT NULL,
     animal_group         TEXT    NOT NULL,
     habitat              TEXT    NOT NULL,
     depth_m              INTGER  NOT NULL,
     estimated_weight_kg  REAL    NOT NULL
  );

  INSERT INTO marine_observation VALUES
  (1, 'Blue Whale',         'Mammal',                 'Open Ocean', 30,  120000.0);
  INSERT INTO marine observation VALUES
  (2, 'Bottlenose Dolphin','Mammal',                  'Open Ocean', 15,  250.0);
  INSERT INTO marine observation VALUES
  (3, 'Green Sea Turle',    'Reptile',                'Coral Reef', 10,  160.0);
  INSERT INTO marine observation VALUES
  (4, 'Clownfish',         'Fish',                 'Coral Reef', 5,  0.3);
  INSERT INTO marine observation VALUES
  (5, 'Hammerhead Shark', 'Fish',                  'Open Ocean',70, 230.0);
  INSERT INTO marine observation VALUES
  (6, 'Giant Octopus',    'Mollusc',               'Seabed',    40, 25.0);
  INSERT INTO marine observation VALUES
  (7, 'Manta Ray',        'Fish',                  'Open Ocean',25  1350.0);
  INSERT INTO marine observation VALUES
  (8, 'Starfish',        'Echinoderm',                  'Seabed',20  0.5);

  SELECT * FROM marine_observation;

  -- ---- PART 2: SELECT DISTINCT -----

  -- All animal groups, including duplicates
  SELECT animal_group   FROM marine_observation;

  -- Only unique animal groups
  SELECT DISTINCT animal_group FROM marine_observation;

  -- Count the animal groups
  SELECT COUNT(DISTINCT animal_group) AS unique_animal_groups
  FROM marine_observation;

  -- ---- PART 3: COUNT ----

  -- Total number of marine observations
  SELECT COUNT(observation_id) AS total_observations
  FROM marine_observation;

  -- Count observations made in the Open Ocean
  SELECT COUNT(observation_id) AS open_ocean_observations
  FROM marine_observation
  WHERE habitat = 'Open Ocean';

  -- ---- PART 4: SUM and AVG ----

  -- Total estimated weight of all observed animals
  SELECT SUM(estimated__weight__kg) AS total_estimated_weight_kg
  FROM marine_observation;

  -- Average depth of all observations
  SELECT AVG(depth_m) AS average_observation_depth_m
  FROM marine_observation;

  -- ---- PART 5: Combining Aggreagate Functions ----

  SELECT 
      COUNT(observation_id)         AS total_observations,
      COUNT(DISTINCT animal_group)  AS unique_animal_groups,
      SUM(estimated__weight_kg)     AS total_estimated_weight_kg,
      AVG(depth__m)                 AS average_observation_depth_m
   FROM marine_observation;