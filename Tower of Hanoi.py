 # 01-tower-of-hanoi.py
 # Topic: Tower of Hanoi,  Solving Tower of Hanoi with Code

 def hanoi(n):
     if n == 0:
         return 0
     return 2 * hanoi(n - 1) + 1

 input("hanoi(n) counts the minimum moves to shift n disks from peg A to peg C. Press Enter ")
 print(" hanoi(1) =", hanoi(1))
 print(" hanoi(2) =", hanoi(2))

 n = int(input("Enter number of disks (try 3 or 4): "))
 guess = input("What is hanoi(" + str(n) + ")? ")
 input("hanoi(n) = 2 * hanoi(n-1) + 1 move the stack twice plus the big disk once. Press Enter ")
 print(" hanoi(" + str(n) + ") =", hanoi(n), " your guess:", guess)