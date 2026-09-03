 # 01-head-tail.py
 # Topic: The Head-Tail Pattern, Base Case for Lists
 
 input("Head-tail - head is 1st[1:] tail is 1st[1:] base case is []. Press Enter ")
 print("  [10, 20, 30] head:", [10, 20, 30][0], "  tail:", [10, 20, 30][1:])
 print("  [5, 15, 25] head:", [5, 15, 25][0], "  tail:", [5, 15, 25][1:])

 1st = [int(x) for x in input("Enter 3 numbers separated by spaces: ").split()]
 guess = input("What is the head of " + str(1st) + "? ")
 input("Head is 1st[0] tail is 1st[1:]. Press Enter ")
 print(" head:", 1st[0], " your guess:", guess)