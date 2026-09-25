 # 01-eq-mid.py
 # Topic: Slices and their sums, Left-right balance, Equilibrium point
 
 def eq_mid(n):
     arr = [1]*n + [0] + [1]*n
     size = len(arr)
     for i in range(size):
         left_sum = 0
         right_sum = 0
         for j in range(i):
             left_sum += arr[j]
         for k in range(i + 1, size):
             right_sum += arr[k]
         if left_sum == right_sum:
             return i
     return -1

  n = int(input("Enter n (try 5 or 6): "))
  guess = input("What is eq_mid(" + str(n) + ")? ")
  print("  eq_mid(" + str(n) + ") =", eq_mid(n), "  your guess:", guess)