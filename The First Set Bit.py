# 02-first-set-bit.py

# Topic: The First Set Bit

input("First set bit - the rightmost 1 in the binary number. Press Enter ")

print(" 5 -> binary:", bin(5)[2:], " first 1 at position 0")

print(" 8 -> binary:", bin(8)[2:], " first 1 at position 3")

n = int(input("Enter a number (try 8 or 14): "))

input("Watch bits drop until the first 1 appears. Press Enter ")

temp = n

pos = 0

while temp > 0:

print(" binary:", bin(temp)[2:], " last bit:", temp & 1)

if temp & 1:

break

pos += 1

temp >>= 1

print(" first set bit in", n, "is at position", pos)