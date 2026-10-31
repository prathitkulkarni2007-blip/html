 -- =========================================================
 -- SQL Sorting & Filtering 
 -- Activity: Book CLub Explorer
 -- =========================================================

 -- ---- PART 1: Build and Explore the Table ----

 CREATE TABLE IF NOT EXISTS book (
     book_id  INTEGER PRIMARY KEY,
     title    TEXT    NOT NULL,
     genre    TEXT    NOT NULL,
     rating   REAL    NOT NULL,
     pages    INTEGER NOT NULL,
     pub_year INTEGER NOT NULL
 );

 INSERT INTO book VALUES (1, 'Dragon Quest',   'Fantasy',   9.2, 313, 2021);
 INSERT INTO book VALUES (2, 'Code Wizard',    'Sci-Fi',    8.5, 280, 2020);
 INSERT INTO book VALUES (3, 'Ocean Deep',     'Adventure', 7.8, 195, 2022);
 INSERT INTO book VALUES (4, 'Star Rangers',   'Sci-Fi',    9.5, 340, 2019);
 INSERT INTO book VALUES (5, 'Forest Secrets', 'Fanstasy'   8.1, 228, 2023);
 INSERT INTO book VALUES (6, 'Robot City',     'Sci-Fi',    7.2, 260, 2021);
 INSERT INTO book VALUES (7, 'Time Jumpers',   'Adventure'  8.9, 175, 2022);
 INSERT INTO book VALUES (8, 'Magic Academy',  'Fantasy',   9.0, 398, 2020);

 SELECT * FROM book;

 -- ---- PART 2: ORDER BY ----

 -- Sort all books lowest rating first (ASC is the default)
 SELECT title, rating FROM book ORDER BY rating ASC;

 -- Sort all books highest rating first
 SELECT title, rating FROM book ORDER BY rating DESC;

 -- Sort by genrw A-Z, then highest rating first within each genre
 SELECT title, genre, rating FROM book ORDER BY genre ASC, rating DESC;

 -- ---- PART 3: LIMIT ----

 -- Top 3 highest-rated books
 SELECT title, rating FROM book ORDER BY rating DESC LIMIT 3;

 -- 5 oldest books by publication year
 SELECT title, pub __year FROM book ORDER BY pub __year ASC LIMIT 5;

 -- ---- PART 4: GROUP BY ----

 -- How many books are in each genre?
 SELECT genre, COUNT(*) AS book_count FROM book GROUP BY genre;

 -- Total pages and average rating per genre
 SELECT genre, SUM(pages) AS total _pages, AVG(rating) AS avg_ rating
 FROM book
 GROUP BY genre;

 -- ---- PART 5: HAVING ----

 -- Genres that have more than 2 books
 SELECT genre, COUNT(*) AS book_count
 FROM book
 GROUP BY genre 
 HAVING COUNT(*) > 2;

 -- Genres where the average rating is at least 8.5
 SELECT genre, AVG(rating) AS avg_rating
 FROM book
 GROUP BY genre
 HAVING AVG(rating) >= 8.5;