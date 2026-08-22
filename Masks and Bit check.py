  # 03-mask-and-check.py
  # Topic: Building a Bit Mask, Check if Nth Bit is Set

  input("Build a bit mask - one 1 at exactly that position.  Press Enter")
  for k in range(4):
      mask = 1 << k
      print("  bit", k, "  mask:", mask, "  binary:", bin(mask)[2:])

  n = int(input("Enter a number (try 42 or 13): "))
  guess = input("Is bit 2 of " + str(n) + " ON? (yes/no): ")
  input("Check if the Nth bit is set - AND with the mask.  Press Enter ")
  result = (n >> 2) & 1
  if result:
      print(" ", n, "  binary:", bin(n)[2:], "  bit 2 is ON  your guess:", guess)
  else:
      print(" ", n, "  binary:", bin(n)[2:], "  bit 2 is OFF your guess:", guess)