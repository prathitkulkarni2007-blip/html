 # 01-big-o-natation.py
 # Topic: Big-O Notation —— each growth pattern has an official name
 # Last class: Formula, Loop, Double Loop, Double Loop. Today each gets its Big-O name.
 
 n = 10

 guess = input("Double Loop at n = 10 checks n x n pairs. How many? ")

 input("Formula: one calculation, done. Press Enter to run ")
 steps = 1
 print(" steps =", steps, " -> o(1) constant time -> steps never change")

 input("Loop: one step per item. Press Enter to run ")
 steps = 0
 for i in range(n):
     steps += 1
 print("  steps =", steps, " -> O(n) linear time -> steps grow with n")

 input("Double Loop: checks every pair.  Press Enter to run ")
 steps = 0
 for i in range(n):
     for j in range(n):
         steps += 1
 print(" steps =", steps, " your guess:", guess, "  -> o(n^2) quadratic time")

 input("Two more notations. Press Enter ")
 print("  Big Omega € ->   best case lower bound")
 print("  Big Theta € ->   exact bound (worst = best)")