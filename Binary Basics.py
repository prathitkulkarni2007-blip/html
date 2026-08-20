  # 01-bits-and-binary.py
  # Topic: Bits and Binary Numbers, AND and OR

  n = int(input("Enter a number (try 5 or 12): "))
  guess = input("Guess its binary: ")

  input("Binary. Press Enter ")
  print("   decimal", n, "-> binary", bin(n) [2:])
  print("   your guess:", guess)

  input("AND — both bits must be 1.  Press Enter ") 
  print("  12 =", bin(12)[2:])
  print("  10 =", bin(10)[2:])
  print("  12 & 10 =", 12 & 10)

  input("OR — at least one bit must be 1.  Press Enter ") 
  print("  12 | 10 =", 12 | 10)