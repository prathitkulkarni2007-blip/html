# 02-best-average-worst.py
   # Topic: Worst, Average and Best Case
   # Same list. Steps depend on where the target is.
   
   scores = [3, 7, 2, 9, 4, 1, 8, 5, 6]
   #          1  2  3  4  5  6  7  8  9

   input("List: " + str(scores) + "  n=9  Linear search — checks left to right. Press Enter ")

   target = int(input("Enter a number to search for: "))

   input("Searching for " + str(target) + ". Press Enter to run ")
   steps = 0
   for score in scores:
       steps += 1
       if score == target:
           break
    print(" target =", target, " found at position", steps, " checks =", steps)

    input("Compare with best and worst case. Press Enter ")
    mid = len(scores) // 2
    print(" Best: 1 check -> O(1) Average:", mid, "checks -> O(n) Worst: 9 checks -> O(n) Yours:", steps)

    input("All three cases. Press Enter ")
    print("  Best O(1)   Average O(n) Worst O(n)  ->   Big-O = worst case = O(n).")
