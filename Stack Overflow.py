 # 03-stuck-overflow.py
 # Topic: Stack Overflow
 
 def sum_down(n):
     if n == 0:
         return 0
     return n + sum_down(n - 1)

 input("Stack overflow - each call adds a frame to the stack  limit is 1000. Press Enter")
 print("  sum_down(3) =", sum_down(3), " uses 3 frames")
 print("  sum_down(5) =", sum_down(5), " user 5 frames")

 n = int(input("Enter a number (try 6 or 9): "))
 input("sum_down(n) = n + (n-1) + ... + 1 uses n frames. Press Enter ")
 print("  sum_down(" + str(n) + ")=", sum_down(n), "  frames used:", n)