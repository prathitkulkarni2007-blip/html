  # 03-max-zeros.py
  # Topic: Streak counter with reset, Best-streak tracker

 def max_zeros(n):
     arr = [1] + [0]*n + [1]
     streak = best = 0
     for x in arr:
         if not x: streak += 1
         else: streak = 0
         if streak > best: best = streak
     return best

 input("max_zeros(n) finds the longest run of 0s in [1, 0..0, 1]. Press Enter ")
 print(" max_zeros(3) =", max_zeros(3))
 print(" max_zeros(4) =", max_zeros(4))
 n = int(input("Enter n (try 5 or 6): "))
 guess = input("What is max_zeros(" + str(n) + ")? ")
 input("streak resets to 0 on each 1 — best keeps the highest streak seen. Press Enter ")
 print("  max_zeros(" + str(n) + ") =", max_zeros(n), "   your guess:", guess)