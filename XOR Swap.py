   # 01-swap.py
   # Topic: Swap Without a Third Variable, XOR Swap
   
   input("XOR swap - exchange two values without a thrid variable.  Press Enter")
   print("  before: a = 5   b = 9")
   a, b = 5, 9
   a ^= b; b ^= a; a ^= b
   print("  after: a =", a, "  b =", b)

   n = int(input("Enter a number (try 3 or 7): "))
   guess = input("After XOR swap of " + str(n) + " and 8 what does n become? ")
   a, b = n, 8
   a ^= b; b ^= a; a ^= b
   input("XOR swap exchanges the values.  Press Enter ")
   print("  n became:", a, "  your guess:", guess)