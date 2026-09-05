  # 03-power-of-4.py
  # Topic: Checking Powers of 4 with Recursion, Two Stopping Conditions

  def is_power4(n):
      if n <= 0:
          return False
      if n == 1:
          return True
      if n % 4 == 0:
          return is_power4(n // 4)
      return False

  input("is_power4 divides by 4 - n==1 returns True  remainder returns False. Press Enter ")
  print(" is_power4(16) =", is_power4(16))
  print(" is_power4(12) =", is_power4(12))

  n = int(input("Enter a number (try 64 or 48): "))
  guess = input("What is is _power4(" str(n) + ")? ")
  input("is_power4 has two stops - n==1 is True remainder or n<=0 is False. Press Enter ")
  printz(" is_power4(" + str(n) + ") =", is_power4(n), "  your guess:", guess)