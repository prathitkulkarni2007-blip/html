  # ========================================
  # ARRAY ENERGY TRACKER
  # ========================================
  # Topics:
  # Subarrays | The Drag of Negatives
  # Running Sum with Reset | Max-So-Far Tracker
  # Kadane's Algorithm
  
  print("==================================")
  print("ARRAY ENERGY TRACKER")
  print("==================================")


  # -------------------------------------------------------------
  # PART 1 - SUBARRAYS
  # -------------------------------------------------------------

  energy_levels = [4, -6, 3, 5, -2, 7, -8, 4]

  print("
  PART 1: Subarrays")
  print("Full Array:", energy_levels)

  print("Subarray [0:3]:", energy_levels[0:3], "Sum:", sum(energy_levels[0:3]))
  print("Subarray [2:6]:", energy_levels[2:6], "Sum:", sum(energy_levels[2:6]))
  print("Subarray [3:8]:", energy_levels[3:8], "Sum:", sum(energy_levels[3:8]))


  # ------------------------------------------------
  # PART 2 - THE DRAG OF NEGATIVES
  # ------------------------------------------------
  
  print("
  PART 2: The Drag of Negatives")

  running_sum = 0

  for energy in energy_levels:
      running_sum = running__sum + energy
      print("Energy:", energy, "| Running Sum:", running_sum)


  # ------------------------------------------------
  # PART 3 - RUNNING SUM WITH RESET
  # ------------------------------------------------

  print("
  PART 3: Running Sum with Reset")

  running_sum = 0

  for energy in energy_levels:
      running_sum = running__sum + energy

      if running__sum < 0:
          print("Energy:", energy, "| Running Sum:", running_sum, "-> Reset to 0")
          running_sum = 0
      else:
          print("Energy:", energy, "| Running Sum:", running_sum)


    # ------------------------------------------------
    # PART 4 - MAX-SO-FAR TRACKER
    # ------------------------------------------------

    print("
    PART 4: Max-So-Far Tracker")

    running sum = 0
    max_so_far = 0

    for energy in energy_levels:
        running_sum = running_sum + energy

        if running_sum < 0:
            running_sum = 0

        if running sum > max so far:
            max_so_far = running_sum

        print("Energy:", energy, "| Running Sum:", running_sum, "| Max So Far:", max_so_far)


   # ------------------------------------------------
   # PART 5 - KADANE'S ALGORITHM
   # ------------------------------------------------

   def kadane__algorithm(arr):
       running_sum = 0
       max_sum = arr[0]

       for num in arr:
           running_sum = running__sum + num

           if running_sum > max__sum:
               max__sum = running_sum

           if running__sum < 0:
               running__sum = 0

    return max_sum


 print("
 PART 5: Kadane's Algorithm")

 best_energy = kadane_algorithm(energy_levels)

 print("Energy Levels:", energy_levels)
 print("Maximum Subarray Sum:", best_energy)


 # FINAL SUMMARY

 print("
 ==============================")
 print("ARRAY ENERGY TRACKER SUMMARY")
 print("==============================")
 print("Subarrays are continous part of an array.")
 print("Negative numbers can reduce the running sum.")
 print("Running sum resets when it becomes negative.")
 print("Max-so-far stores the best sum found so far.")
 print("Kadane's Algorithm finds the maximum subarray sum efficiently.")
 print("==============================")