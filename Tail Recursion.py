   # 01-linear-tail.py
   # Topic: Linear Recursion, Tail Recursion

   def tail_sum(n, acc=0):
       if n == 0:
           return acc
       return tail_sum(n - 1, acc + n)

  input("Tail recursion - the last action is the recursive call with an accumulator. Press Enter ")
  print("  tail__sum(4) =", tail_sum(4), "  = 4 + 3 + 2 + 1")
  print("  tail__sum(4) =", tail_sum(4), "  = 5 + 4 + 3 + 2 + 1")

  n = int(input("Enter a number (try 3 or 6): "))
  guess = input("What is tail_sum(" + str(n) + ")? ")
  input("tail_sum adds n to acc at each step - acc builds as n counts down. Enter ")
  print(" tail__sum(" + str(n) + ") =", tail_sum(n), "  your guess:", guess)