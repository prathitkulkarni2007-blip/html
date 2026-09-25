 # 02-eq-val.py
 # Topic: Slices and their sums, Equilibrium point
 
 def eq_val(n):
     arr = [1]*n + [n] + [1]*n
     size = len(arr)
     for i in range(size):
         left_sum = 0
         right_sum = 0
         for j in range(i):
             left_sum += arr[j]
         for k in range(i + 1, size):
             right_sum += arr[k]
         if left_sum == right_sum:
             return arr[i]
     return -1

 n = int(input("Enter n (try 5 or 6): "))
 guess = input("What is eq_val(" + str(n) + ")? ")
 print("  eq_val(" + str(n) + ") =", eq_val(n), "  your guess:", guess)