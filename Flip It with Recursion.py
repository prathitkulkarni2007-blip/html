 # ================================
 # FLIP IT WITH RECURSION
 # ================================
 # Topics:
 # Extracting Digits with % and //
 # Reversing a Number with Recursion
 # Reversing a String with Recursion
 # Checking Powers of 4 with Recursion
 # Two Stopping Conditions
 
 print("===============================")
 print("FLIP IT WITH RECURSION")
 print("===============================")


 # ---------------------------------------------------
 # PART 1 — EXTRACTING DIGITS WITH % AND //
 # ---------------------------------------------------

 number = 4827
 temp = number

 print("
 PART 1: Extracting Digits")
 print("Original Number:", number)

 while temp > 0:
     last_digit = temp % 10
     remaining_number = temp // 10

     print("Last Digit:", last_digit, "| Remaining Number:", remaining_number)

     temp = remaining_number


 # -----------------------------------------------
 # PART 2 — REVERSING A NUMBER WITH RECURSION
 # -----------------------------------------------

 def count_digits(num):
     if num < 10:
         return 1
     return 1 + count_digits(num // 10)


 def reverse_number(num):
     if num < 10:
         return num

     last_digit = num % 10
     remaining_number = num // 10
     digits_left = count_digits(remaining_number)

     return last_digit * (10 ** digits_left) + reverse_number(remaining_number)


  print("
  PART 2: Reversing a Number")
  num = 4827
  print("Original Number:", num)
  print("reversed Number:", reverse_number(num))


  # ---------------------------------------------------
  # PART 3 – REVERSING A STRING WITH RECURSION
  # ---------------------------------------------------

  def reverse_string(text):
      if len(text) <= 1:
          return text

      return reverse_string(text[1:]) + text[0]


  print("
  PART 3: Reversing a String")
  word = "CODING"
  print("Original String:", word)
  print("Reversed String:", reverse_string(word))


  # ------------------------------------------------
  # PART 4 — CHECKING POWERS OF 4 WITH RECURSION
  # ------------------------------------------------

  def is__power__of__4(num):
      if num <= 0:
          return False

      if num == 1:
          return True

      if num % 4 != 0:
          return False

      return is_power_of_4(num // 4)


  print("
  PART 4: Checking Powers of 4")

  numbers = [1, 4, 8, 16, 20, 64, 100, 256]

  for value in numbers:
      print(value, "is power of 4:", is_power_of__4(value))


  # --------------------------------------------------
  # PART 5 — TWO STOPPING CONDITIONS
  # --------------------------------------------------

  print("
  PART 5: Two Stopping Conditions")
  print("Stopping condition 1: num <= 0 stops invalid power checks.")
  print("Stopping condition 2: num == 1 confirms the number is a power of 1.")



  # FINAL SUMMARY

  print("
  ==================================")
  print("FLIP IT WITH RECURSION SUMMARY")
  print("================================")
  print("% gives the last digit of a number.")
  print("// removes the last digit of a number.")
  print("Recursion can reverse numbers and strings.")
  print("A power of 4 can be checked by repeatedly dividing by 4.")
  print("Every recursive function needs clear stopping conditions.")
  print("================================")