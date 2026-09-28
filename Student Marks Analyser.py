 # ================================
 # STUDENT MARKS ANALYSER
 # ================================
 # Topics:
 # What is Pandas & Importing It
 # Pandas Series —— 1D Labelled Data
 # Pandas DataFrame —— 2D Tables
 # Reading & Viewing Data
 # Cleaning Data
 
 import pandas as pd

 print("================================")
 print("STUDENT MARKS ANALYSER")
 print("================================")

 # ----------------------------------------------
 # PART 1 — WHAT IS PANDAS?
 # ----------------------------------------------

 print("
 PART 1: What is Pandas?")
 print("Pandas is a Python library used to work with data.")
 print("It helps you create tables, read files, view data, and clean data.")

  # ----------------------------------------------
  # PART 2 — PANDAS SERIES
  # ----------------------------------------------
  # A Series is like a single column of labelled data.

  print("
  PART 2: Pandas Series")

  marks = [88, 76, 92, 67, 85]

  students marks = pd.Series(
      marks,
      index=["Aarav", "Meera", "Kabir", "Anaya", "Rohan"]
  )

  print(student__marks)

   # ----------------------------------------------
   # PART 3 — PANDAS DATAFRAME
   # ----------------------------------------------
   # A DataFrame is like a table with rows and columns.

   print("
   PART 3: Pandas DataFrame")

   data = {
       "Student": ["Aarav", "Meera", "Kabir", "Anaya", "Rohan"],
       "Math": [88, 76, 92, 67, 85],
       "Science": [91, 80, 89, 72, 87],
       "English": [84, 78, 95, 70, 82],
       "Attedence": [96, 90, 98, 85, 92]
   }

   df = pd.DataFrame(data)

   print(df)

   # ---------------------------------------------------
   # PART 4 — CREATE AND READ A CSV FILE
   # ---------------------------------------------------

   print("
   PART 4: Reading Dats from a CSV File")

   df.to_csv("student_marks.csv", index=False)

   student__data = pd.read__csv("student_marks.csv")

   print("CSV file read successfully!")
   print(student__data)

   # ----------------------------------------------
   # PART 5 — VIEWING DATA
   # ----------------------------------------------

   print("
   PART 5: Viewing Data")

   print("
   First 3 rows:")
   print(student_data.head(3))

   print("
   Last 2 rows:")
   print(student_data.tail(2))

   print("
   Date Information:")
   print(student__data.info())

   # ------------------------------------------------------------
   # PART 6 — CLEANING DATA
   # ------------------------------------------------------------

   print("
   PART 6: Cleaning Data")

   messy_data = {
      "Student": ["Aarav", "Meera", "Kabir", "Anaya", "Rohan"],
      "Math": [88, None, 92, 67, 85],
      "Science": [91, 80, None, 72, 87],
      "English": [84, 78, 95, None, 82]
   }

   messy__df = pd.DataFrame(messy_data)

   print("
   Data with Missing Values:")
   print(messy_df)

   cleaned__df = messy__df.fillna(0)

   print("
   Cleaned Data:")
   print(cleaned_df)

   # ----------------------------------------------------------
   # PART 7 —— SIMPLE ANALYSIS
   # ----------------------------------------------------------

   print("
   PART 7: Student Total and Average Marks")

   cleaned__df["Total"] = cleaned__df["Math"] + cleaned__df["Science"] + cleaned__df["English"]
   cleaned__df["Average"] = cleaned__df["Total"] / 3

   print(cleaned__df)

   # FINAL SUMMARY

   print("
   ===================================")
   print("STUDENT MARKS ANALYSER SUMMARY")
   print("===================================")
   print("Pandas was imported using import pandas as pd.")
   print("A Series was used to store one column of marks.")
   print("A DateFrame was used to store marks in table form.")
   print("CSV data was created, read, and viewed.")
   print("Missing values were cleaned using fillna().end=")
   print("Total and average marks were calculated.")
   print("================================")