 # 03-max-after.py
 # Topic: The Drag of Negatives, Running Sum with Reset, Kadane's Algorithm
 
 def max_after(n):
     arr = [-n] + [1]*n
     current = best = arr[0]
     for x in arr[1:]:
         if current < 0: current = x
         else: current = current + x
         if current > best: best = current
     return best

  input("max_after(n) finds the max subarray sum in [-n, 1, 1, ..., 1].  Press Enter")
  print("   max_after(3) =", max_after(3))
  print("   max_after(4) =", max_after(4))
  n = int(input("Enter n (try 5 or 6):  "))
  guess = input("What is max_after(" + str(n) + ")? ")
  input("big negative resets — then n ones add up to n.  Press Enter ")
  print("  max_after(" + str(n) + ") =", max_after(n), "  your guess:", guess)