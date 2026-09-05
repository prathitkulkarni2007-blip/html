  # 01-digit-flip.py
  # Topic: Digit Extraction with % and //, Reversing a Nummber with Recursion
  
  def flip_number(num):
      if num // 10 == 0:
          return num
      last = num % 10
      rest = flip_number(num // 10)
      return last * pow(10, len(str(rest))) + rest

 input("flipNumber peels last digit with % 10 then recurses on // 10. Press Enter ")
 print("  flip_number(123) =", flip_number(123))
 print("  flip_number(456) =", flip_number(456))

 n = int(input("Enter a number (try 789 or 1234): "))
 guess = input("What is flip_number(" + str(n) + ")? ")
 input("flip_number peels last digit and places it at the front each step. Press Enter ")
 print(" flip_number(" + str(n) + ")=", flip_number(n), "   your guess:", guess)