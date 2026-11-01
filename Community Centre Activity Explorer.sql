-- ================================================================
-- SQL Sorting & Filtering 
-- Activity: Community Centre Activity Explorer
-- ================================================================

-- ---- PART 1: Build and Explore the Table ----

CREATE TABLE IF NOT EXISTS community_activity (
    activity_id     INTEGER PRIMARY KEY,
    activity_name   TEXT    NOT NULL,
    activity_type   TEXT    NOT NULL,
    day             TEXT    NOT NULL,
    participants    INTEGER NOT NULL,
    duration_mins   INTEGER NOT NULL
 );
 
 INSERT INTO community_activity VALUES (1, 'Yoga Class',   'Wellness', 'Monday',  18, 60);
 INSERT INTO community_activity VALUES (2, 'Art Workshop', 'Creative', 'Tuesday', 12, 90);
 INSERT INTO community_activity VALUES (3, 'Chess Club',   'Games',    'Wednesday', 16, 75);
 INSERT INTO community_activity VALUES (4, 'Dance Practice','Wellness', 'Thursday', 20, 60);
 INSERT INTO community_activity VALUES (5, 'Coding Club',   'Learning', 'Friday',   14, 90);
 INSERT INTO community_activity VALUES (6, 'Book Circle',   'Learning', 'Saturday', 10, 60);
 INSERT INTO community_activity VALUES (7, 'Painting Club',  'Creative',  'Saturday', 15, 75);
 INSERT INTO community_activity VALUES (8, 'Football Practice', 'Sports'  'Sunday',   22, 90);
 INSERT INTO community_activity VALUES (9, 'Meditation Hour',   'Wellness', 'Sunday', 13, 45);

 SELECT * FROM community_activity;

 -- ---- PART 2: ORDER BY ----

 -- Sort all activities by participants, lowest first
 SELECT activity_name, participants
 FROM community_activity
 ORDER BY participants ASC;

 -- Sort all activities by participants, highest first
 SELECT activity_name, participants
 FROM community_activity
 ORDER BY participants DESC;

 -- Sort by activity type A-Z, then highest participants first
 SELECT activity_name, activity_type, participants
 FROM community_activity
 ORDER BY activity_type ASC, participants DESC;

 -- ---- PART 3: LIMIT ----

 -- Top 3 activities with the most participants
 SELECT activity_name, participants
 FROM community_activity
 ORDER BY participants DESC
 LIMIT 3;

 -- 5 shortest activities by duration
 SELECT activity_name, duration_mins
 FROM community_activity
 ORDER BY duration_mins ASC
 LIMIT 5;

 -- ---- PART 4: GROUP BY ----

 -- How many activites  are in each activity type?
 SELECT activity_type, COUNT(*) AS activity_count
 FROM community_activity
 GROUP BY activity_type;

 -- Total participants and average duration per activity type
 SELECT activity_type,
        SUM(participants) AS total_participants,
        AVG(duration_mins) AS average_duration_mins
 FROM community_activity
 GROUP BY activity_type;

 -- ---- PART 5: HAVING ----

 -- Activity types with more than 2 activites
 SELECT activity_type, COUNT(*) AS activity_count
 FROM community_activity
 GROUP BY activity_type
 HAVING COUNT(*) > 2;

 -- Activity types with an average of at least 15 participants
 SELECT activity_type, AVG(participants) AS average_participants
 FROM community_activity
 GROUP BY activity_type
 HAVING AVG(participants) >= 15;