 # 03-rainwater.py
 # Topic: Left tallest bars,  Right tallest bars, Rainwater trapped
 
 def rainwater(n):
     bars = [0, n, 0, n, 0]
     return min(max(bars[:3]), max(bars[2:])) - bars[2]

 input("rainwater(n) traps water between two bars of height n.  Press Enter ")
 print("  rainwater(3) =", rainwater(3))
 print("  rainwater(4) =", rainwater(4))
 n = int(input("Enter bar height (try 5 or 6): "))
 guess = input("What is rainwater(" + str(n) + ")? ")
 input("water = min(left tallest, right tallest) - bar height at the gap.  Press Enter ")
 print("  rainwater(" + str(n) + ") =", rainwater(n), "  your guess:", guess)