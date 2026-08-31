 # ==================================
 # STACK FRAME VISUALIZER
 # ==================================
 # Topics:
 # Linear Recursion | Tail Recursion | Head Recursion
 # Increasing-Decreasing Recursion | Tree Recursion
 
 print("=================================")
 print("STACK FRAME VISUALIZER")
 print("=================================")


 # ---------------------------------------------------
 # PART 1 - LINEAR RECURSION
 # ---------------------------------------------------
 # Linear recursion makes one recursive call at each level.

 def linear_recursion(n):
     if n ==0:
         return

     print("Linear call at levelL:", n)
     linear_recursion(n - 1)


 print("\nPART 1: Linear Recursion")
 linear_recursion(5)


 # ---------------------------------------------------
 # PART 2 - TAIL RECURSION
 # ---------------------------------------------------
 # Tail recursion does the work first.
 # The recursive call is the last step.

 def tail_recursion(n):
     if n == 0:
         return

     print("Tail work before call:", n)
     tail_recursion(n - 1)


 print("\nPART 2: Tail Recursion")
 tail_recursion(5)


 # ---------------------------------------------------
 # PART 3 - HEAD RECURSION
 # ---------------------------------------------------
 # Head recursion calls itself first.
 # The work happens while the call stuck unwinds.

 def head_recursion(n):
     if n == 0:
         return

     head_recursion(n - 1)
     print("Head work after call:", n)


 print("\nPART 3: Head Recursion")
 head_recursion(5)


 # ---------------------------------------------------
 # PART 4 - INCREASING-DECREASING RECURSION
 # ---------------------------------------------------
 # This prints while going down and again while coming back.

 def increasing_decreaing(n):
     if n == 0:
         return

     print("Going down:", n)
     increasing_decreaing(n - 1)
     print("Coming back:", n)


 print("\nPART 4: Increasing-Decreasing Recursion")
 increasing_decreaing(5)


 # ---------------------------------------------------
 # PART 5 - TREE RECURSION
 # ---------------------------------------------------
 # Tree recursion makes more than one recursive call at each level.

 def tree_recursion(n):
     if n == 0:
         return

     print("Tree node:", n)
     tree_recursion(n - 1)
     tree_recursion(n - 1)


 print("\nPART 5: Tree Recursion")
 tree_recursion(3)


 # FINAL SUMMARY

 print("\n===============================")
 print("RECURSION PATTERN SUMMARY")
 print("===============================")
 print("Linear Recursion: One recursive call at each level.")
 print("Tail Recursion: Work happens before the recursive call.")
 print("Head Recursion: Work happens after the recursive call.")
 print("Increasing-Decreasing: Work happens before and after the call.")
 print("Tree Recursion: More than one recursive call at each level.")
 print("===============================")