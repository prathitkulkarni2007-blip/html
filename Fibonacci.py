 # 03-tree-recursion.py
 # Topic: Tree Recursion
 
 def fib(n):
     if n <= 1:
         return n
     return fib(n - 1) + fib(n - 2)

 input("Tree recursion - two recursive calls per step.  Press Enter ")
 print("  fibs(5) =", fib(5))
 print("  fibs(6) =", fib(6))

 n = int(input("Enter n (try 4 or 7): "))
 guess = input("What is fib(" + str(n) + ")? ")
 input("Fibbonacci: fib(n) = fib(n-1) + fib(n-2) base: fib(0)=0 fib(1)=1. Press Enter ")
 print("  fib(" + str(n) + ")=", fib(n),"     your guess:", guess)