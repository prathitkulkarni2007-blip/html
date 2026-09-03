 # 03-list-max.py
 # Topic: Largest Element with Recursion
 
 def list_max(1st):
     if len(1st) == 1:
         return 1st[0]
     rest = list_max(1st[1:])
     return 1st[0] if 1st[0] > rest else rest 

 input("Recursive max - compare head to max of tail.  Press Enter ")
 print("  list_max([3, 7, 2]) =", list_max([3, 7, 2]))
 print("  list_max([8, 1, 5]) =", list_max([8, 1, 5]))

 n = int(input("Enter a number (try 6 or 15): "))
 1st = [n, 4, 9, 2]
 guess = input("What is the largest in " + str(lst) + "? ")
 input("list_max compares head to max of tail at each step. Press Enter")
 print("  largest:", list_max(1st), " your guess:", guess)