 # 03-recursion-tree.py
 # Topic: Recursion Trees and How Problems Grow
 
 def paths(m, n):
     if m == 1 or n == 1:
         return 1
     return paths(m - 1, n) + paths(m, n - 1)

 input("paths(m, n) counts routes through an m x n grid moving only right or down.  Press Enter ")
 print("  paths(3, 3) =", paths(3, 3))
 print("  paths(4, 4) =", paths(4, 4))
 n = int(input("Enter grid size for both rows and cols (try 5 or 6): "))
 guess = input("What is paths(" + str(n) + ", " + str(n) + ")? ")
 input("each call branches into two — move down or move right — the tree grows fast. Press Enter")
 print(" paths(" + str(n) + ", " + str(n) + ") =", paths(n, n), " your guess:", guess)