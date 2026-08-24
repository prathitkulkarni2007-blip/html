   # 02-odd-occurring .py
   # Topic: One Odd-Occuring Number
   
   input("XOR all numbers - pairs cancel, the odd one stays.  Press Enter ")
   print("  list: [2, 3, 4, 3, 2]")
   print("   odd-occuring:", 2^3^4^3^2)

   n = int(input("Enter a number (try 7 or 11): "))
   nums = [3, n, 5, 3, 5]
   guess = input("Which number in " + str(nums) + " appears once? ")
   result = 0
   for x in nums:
       result ^= x
   input("XOR cancels pairs - the odd one survives. Press Enter ")
   print("  list:", nums, "  odd-occurring:", result, " your guess:", guess)