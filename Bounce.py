  # 02-head-increasing.py
  # Topic: Head Recursion, Increasing-Decreasing
  
  def mirror(n):
      if n == 0:
          return 0
      rest = mirror(n - 1)
      return rest + 2 * n

  input("Head recursion - recurse first  then add 2*n on the way back. Press Enter")
  print("  mirror(3) =", mirror(3))
  print("  mirror(4) =", mirror(4))

  n = int(input("Enter a number (try 5 or 6): "))
  guess = input("What is mirror(" + str(n) + ")? ")
  input("mirror(n) = mirror(n-1) + 2*n adds 2*n as it unwinds back up. Press Enter")
  print("  mirror(" + str(n) + ") =", mirror(n), "  your guess:", guess)