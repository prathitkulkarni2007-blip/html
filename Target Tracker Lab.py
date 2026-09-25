 # =========================================
 # TARGET TRACKER LAB
 # =========================================
 # Topics:
 # Slices and their sums | Left-right balance
 # Equilibrium point | Subarray window
 # Target sum search

 print("==============================")
 print("TARGET TRACKER LAB")
 print("==============================")

 # PART 1 - SLICES AND THEIR SUMS
 numbers = [-4, 6, 2, 0, 0, 1, 1]

 print("\nPART 1: Slices and Their Sums")
 print("Full Array:", numbers)

 index = 2
 left_slice = numbers[:index]
 right_slice = numbers[index + 1:]

 print("Left of index", index, ":", left_slice)
 print("Right of index", index, ":", right_slice)
 print("Left Sum:", sum(left_slice))
 print("Right Sum:", sum(right_slice))

 # PART 2 - LEFT-RIGHT BALANCE
 print("\nPART 2: Left-Right Balance")

 for i in range(len(numbers)):
     left_sum = sum(numbers[:i])
     right_sum = sum(numbers[i + 1:])
     print("Index", i, "-> Left Sum:", left_sum, "| Right Sum:", right_sum)

  # PART 3 - EQUILIBRIUM POINT
  print("\nPART 3: Equilibrium Point")

  for i in range(len(numbers)):
      left_sum = sum(numbers[:i])
      right_sum = sum(numbers[i + 1:])

      if left_sum == right_sum:
          print("Equilibrium found at index:", i)
          print("Element:", numbers[i])

    # PART 4 - SUBARRAY WINDOW
    values = [3, 6, 2, 2, 4, 1]

    print("\nPART 4: Subarray Window")
    print("Array:", values)

    window_sum = 0

    for i in range(len(values)):
        window sum = window sum + values[i]
        print("Window from index 0 to", i, ":", values[:i = 1], "| Sum:", window_sum)

  # PART 5 - TARGET SUM SEARCH
  target = 10

  print("\nPART 5: Target Sum Search")
  print("Target Sum:", target)

  found = False

  for start in range(len(values)):
      current_sum = 0

      for end in range(start, len(values)):
          current_sum = current_sum + values[end]

          if current_sum == target:
              print("Target subarray found:",values[start:end + 1])
              print("Start Index:", end)
              print("End Index:", end)
              found = True

    if found == False:
        print("No subarray found with target sum.")

    print("\n==============================")
    print("TARGET TRACKER LAB SUMMARY")
    print("================================")
    print("Slices help split an array into smaller parts.")
    print("Left-right balance compares sums on both sides of an index.")
    print("An equilibrium point has equal left and right sums.")
    print("A subarray window is a continuous part of an array.")
    print("Target sum search finds a subarray with the required sum.")
    print("================================")