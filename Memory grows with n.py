 # 03-list-in-memory.py
 # Topic: Space Complexity — how much memory an algorithm uses
 # List stores every score in mermory, so memory grows as n grows (On space)
 
 n = 4

 # List stores every score in memory — memory grows with n
 guess = input("Predict: how many items in the List for n = 4? ")
 points = list(range(1, n + 1))\
 print(" your guess:", guess, "  List:", points,"  items:", len(points))

 input("Predict: what happens to List size as n grows? Press Enter ")
 for size in [4, 10, 100, 1000]:
     print(f"n = {size:<5}  List uses {size:>5} items in memory")