 # 01-set-and-power.py
 # Topic: Set Bits and Zero Bits, Power of 2 Check
 input("Set a bit - OR turns it ON. Press Enter ")
 print(" 5 =", bin(5)[2:])
 print(" 5 | 2 =", 5 | 2, " binary:", bin(5 | 2)[2:])
 input("Zero a bit - AND turns it OFF. Press Enter ")
 print(" 7 =", bin(7)[2:])
 print(" 7 & 5 =", 7 & 5, " binary:", bin(7 & 5)[2:])
 n = int(input("Enter a number (try 4 or 6): "))

guess = input("Is it a power of 2? (yes/no): ")

input("Power of 2 - only one bit is ON. Press Enter ")

if n > 0 and (n & (n - 1)) == 0:

print(" ", n, " binary:", bin(n)[2:], " power of 2 your guess:", guess)

else:

print(" ", n, " binary:", bin(n)[2:], " not power of 2 your guess:", guess)