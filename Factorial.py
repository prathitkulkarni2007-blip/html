 # 02-factorial.py
 # Topic: Counting with Recursion, Factorial Using Recursion
 
 def factorial(n):
     if n == 0:
        return 1
    return n * factorial(n - 1)

 input("Factorial - n! = n x (n-1) x ... x 1 base case: 0! = 1.  Press Enter ")
 print("  4! =", factorial(4), "  = 4 x 3 x 2 x 1")
 print("  5! =", factorial(5),"   = 5 x 4 x 3 x 2 x 1")

 n = int(input("Enter a number (try 3 or 6): "))
 guess = input("What is " + str(n) + "!? ")
 input("n! = n x factorial(n-1)  base case: 0! = 1. Press Enter ")
 print(" ", str(n) + "! =", factorial(n), "  your guess:", guess)