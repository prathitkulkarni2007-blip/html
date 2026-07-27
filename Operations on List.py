 # ----- School Class Organiser ----

  # STEP 1 - Create a list of classmates
  classmates = ["Aarav", "Priyaka
  ", "Rahul", "Snehalata
  ", "Dev"]
  print("Class list:", classmates)

  # STEP 2 - Access the list
  print("Total students:", len(classmates))
  print("First student:", classmates[0])
  print("Last student:", classmates[-1])
  print("First three:", classmates[:3])

  # STEP 3 - Modify the list
  classmates.append("Meera")
  print("\nAfter adding Meera:", classmates)
  classmates.remove("Dev")
  print("After removing Dev:", classmates)
  classmates.sort()
  print("Sorted alphabetically:", classmates)
  classmates.reverse()
  print("Reversed:", classmates)

  # STEP 4 - Create a teacher dictionary
  teacher = {"name": "Mr. Sharma", "subject": "Python", "experience": 5}
  print("\nTeacher profile:", teacher)

  # STEP 5 - Dictionary operations
  print("Subject:", teacher["subject"])
  print("Experience:", teacher.get("experience", "Not found"))
  teacher["experience"] = 6
  teacher["email"] = "sharma@school.com"
  teacher.pop("experience")
  print("Updated teacher profile:", teacher)

  # STEP 6 - Convert lists to a student directory
  roll_numbers = [1, 2, 3, 4, 5]
  names = ["Aarav", "Priya", "Rahul", "Sneha", "Meera"]
  student_directory = dict(zip(roll_numbers, names))
  print("\nStudent Directory:", student_directory)
  print("Student at Roll 3:", student_directory[3])
