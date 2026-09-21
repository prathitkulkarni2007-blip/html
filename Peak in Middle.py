  # 01—max—mid.py
  # Topic: Subarrays, Running Sum with Reset, Max-So-Far Tracker, Kadane's Algorithm
  
  def max_mid(n):
      arr = [-1, n, -1]
      current = best = arr[0]
      for x in arr[1:]:
          if current < 0: current = x
          else: current = current + x
          if current > best: best = current
      return best

 input("max_mid(n) finds the max subarray sum in [-1, n, -1].  Press Enter ")
 print("  max_mid(3) =", ma_mid(3))
 print("  max_mid(4) =", ma_mid(4))
 n = int(input("Enter n (try 5 or 6): "))
 guess = input("What is max_mid(" + str(n) + ")? ")
 input("negative at start resets —— best locks in the peak value n. Press Enter ")
 print("  max_mid(" + str(n) + ") =", max_mid(n), "   your guess:", guess)