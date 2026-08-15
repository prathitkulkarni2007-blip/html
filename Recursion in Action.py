  # 02-recursion.py
  # Topic: Recursion and Recursion Time Complexity
  # A function that calls itself. Each call stacks up.
  
  n = int(input("Enter n (try 3 or 5): "))
  guess = input("How many times does countdown call itself for n = " + str(n) + "? ")

  input("Recursion — watch each call.  Press Enter to run")
  def countdown(num):
      print(" call — n =", num)
      if num > 0:
          countdown(num - 1)
  countdown(n)
  print(" calls =", n + 1, " your guess:", guess, " -> O(n)")

  input("Watch calls grow with n. Press Enter ")
  for size in [5, 10, 100]:
      print(" n =", size, " calls =", size + 1, " -> O(n)")