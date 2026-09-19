  # ===============================
  # BINARY STREAK TRACKER
  # ===============================
  # Topics:
  # Binary arrays | Streak counter with reset
  # Best-streak tracker | Same-direction two pointers
  # Write-pointer pattern
  
  print("==============================")
  print("BINARY STREAK TRACKER")
  print("==============================")


  # -------------------------------------------------
  # PART 1 - BINARY ARRAYS
  # -------------------------------------------------

  binary_scores = [1, 1, 0, 1, 1, 0, 1, 1]

  print("
  PART 1: Binary Arrays")
  print("Binary Array:", binary_scores)
  print("This array contains only 0s and 1s.")


  # -------------------------------------------------
  # PART 2 - STREAK COUNTER WITH RESET
  # -------------------------------------------------

  current_streak = 0

  print("
  PART 2: Streak Counter with Reset")

  for score in binary_scores:
      if score == 1:
          current_streak = current_streak + 1
      else:
          current_streak = 0

    print("Score:", score, "| Current Streak:", current_streak)


  # -------------------------------------------------
  # PART 3 - BEST-STREAK TRACKER
  # -------------------------------------------------

  current_streak = 0
  best_streak = 0

  print("
  PART 3: Best-Streak Tracker")

  for score in binary_scores:
      if score == 1:
          current_streak = current_streak + 1
          best_streak = max(best_streak, current_streak)
      else:
          current_streak = 0

  print("Longest streak of 1s:", best_streak)


  # ----------------------------------------------
  # PART 4 - SAME-DIRECTION TWO POINTERS
  # ----------------------------------------------

  numbers = [0, 1, 0, 3, 12, 0, 5]

  print("
  PART 4: Same-Direction Two Pointers")
  print("Original Array:", numbers)

  write_pointer = 0

  for read_pointer in range(len(numbers)):
      if numbers[read_pointer] != 0:
          numbers[write_pointer] = numbers[read_pointer]
          write_pointer = write_pointer + 1

  print("After moving non-zero values forward:", numbers)


  # ------------------------------------------------
  # PART 5 - WRITE-POINTER PATTERN
  # ------------------------------------------------

  print("
  PART 5: Write-Pointer Pattern")

  while write_pointer < len(numbers):
      numbers[write_pointer] = 0
      write_pointer = write_pointer + 1

  print("Final Array after moving zeros to the end:", numbers)


  # FINAL SUMMARY

  print("
  ================================")
  print("BINARY STREAK TRACKER SUMMARY")
  print("================================")
  print("Binary arrays store only 0s and 1s.")
  print("A streak counter increases when 1 appears.")
  print("The streak resets when 0 appears.")
  print("The best streak stores the longest streak found.")
  print("Same-direction pointers move through the array from left to right.")
  print("The write pointer tracks where the next non-zero value should go.")
  print("================================")