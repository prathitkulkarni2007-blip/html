 # 03-win-sum.py
 # Topic: Subarray window, Target sum search
 
 def win_sum(n):
     arr = [0]*n + [1]*n
     size = len(arr)
     for i in range(size - n + 1):
         curr_sum = 0
         for j in range(i, i + n):
             curr_sum += arr[j]
         if curr_sum == n:
             return i
     return -1

  n = int(input("Enter n (try 5 or 6): "))
  guess = input("What is win_sum(" + str(n) + ")? ")
  print(" win_sum(" + str(n) + ") =", win_sum(n), "  your guess:", guess)