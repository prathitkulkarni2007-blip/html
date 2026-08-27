 # 03-bit-diff.py
 # Topic: Bit Difference

 input("Bit difference - XOR shows which bits differ. Press Enter")
 print("  5 ^ 3 =", 5 ^ 3, "  binary", bin(5 ^ 3)[2:], " bits different:", bin(5 ^ 3).count('1'))
 print("  9 ^ 5 =", 9 ^ 5, "  binary", bin(9 ^ 5)[2:], " bits different:", bin(9 ^ 5).count('1'))

 n = int(input("Enter a number (try 9 or 6): "))
 print("  binary:", bin(n)[2:])
 guess = input("What is bit 2 of " + str(n) + "? (0 or 1): ")
 input("Bit probe: (n >> 2) & 1 gives the bit value.  Press Enter ")
 print(" ", n, " bit 2 =", (n >> 2) & 1, " your guess:", guess)