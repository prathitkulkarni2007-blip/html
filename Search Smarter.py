 # 01-binary-search.py
 # Topic: O(log n) and Binary Search
 # Binary search always checks the checks the middle and drops half the list.
 
 scores = [1, 3, 5, 7, 9, 11, 13, 15, 17]

 input("List: " + str(scores) + " n = 9 Press Enter ")
 guess = input("Max checks to find any number in the list? ")
 target = int(input("Pick a number from the list: "))

  input("Binary search –  checks the middle, drops half each round.  Press Enter ")
  low, high = 0, len(scores) - 1
  steps = 0
  while low <= high:
      mid = (low + high) // 2
      steps += 1
      print(" round", steps, "-> checked", scores[mid])
      if scores[mid] == target:
          break
      elif scores[mid] < target:
          low = mid + 1
      else:
          high = mid - 1
  print(" found", target, "at position", mid + 1, "in", steps, "steps  your guess:", guess," -> O(log n)")

  input("Steps grow slowly with n. Press Enter ")
  for n, s in [(9, 4), (100, 7), (1000, 10)]:
      print(" n=", n, " max steps =", s, " -> O(log n)")