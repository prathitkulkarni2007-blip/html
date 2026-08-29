 # =================================
 # MY COUNTDOWN TIMER CHALLENGE
 # =================================
 # Topics:
 # What Is Recursion? | Base Case | Build and Unwind
 # Counting with Recursion | Factorial Using Recursion | Stack Overflow
 
 print("=================================")
 print("MY COUNTDOWN TIMER CHALLENGE")
 print("=================================")


 # --------------------------------------------------
 # PART 1 — WHAT IS RECUSION?
 # --------------------------------------------------
 # Recursion means a function calls itself.
 # A recursive function must have:
 # 1. A base case to stop
 # 2. A recursive call with a smaller problem
 

 # -----------------------------------------------------
 # PART 2 — COUNTDOWN WITH RECURSION
 # -----------------------------------------------------

 def countdown(number):
     # Base Case
     if number == 0:
         print("Time is up!")
         return

     print(number)
     countdown(number - 1)


 print("
 Countdown from 5:")
 countdown(5)


 # -----------------------------------------------------
 # PART 3 — HOW RECURSION BUILDS AND UNWINDS
 # -----------------------------------------------------

 def build_and_unwind(level):
     # Base Case
     if level == 0:
         print("Base case reached. Now unwinding begins.")
         return

     print("Building level:", level)
     build_and_unwind(level - 1)
     print("Unwinding level:", level)


 print("
 Build and Unwind Demo:")
 build_and_unwind(3)


 # -----------------------------------------------------
 # PART 4 — COUNTING WITH RECURSION
 # -----------------------------------------------------

 def count_up(number):
     # Base Case
     if number > 10:
         return

     print(number)
     count_up(number + 1)


 print("
 Counting from 1 to 10:")
 count_up(1)


 # -----------------------------------------------------
 # PART 5  — FACTORIAL USING RECURSION
 # ----------------------------------------------------- 
 
 def factorial(number):
     # Base Case
     if number == 0 or number == 1:
         return 1

     return number * factorial(number - 1)


 print("
 Factorial Result:")
 print("5! =", factorial(5))


  # -----------------------------------------------------
  # PART 6 — STACK OVERLOW SAFETY DEMO
  # -----------------------------------------------------
  # Warning:
  # If a recursive function does not have a base case,
  # it keeps calling itself and may cause a stack overflow.
  # Do not run this function unless you understand the risk.

  def unsafe_countdown(number):
      print(number)
      # Missing base case - this can cause stack overflow
      # unsafe_countdown(number - 1)


  print("
  Stack Overflow Note:")
  print("A recursive function must have a base case to stop safely.")
  print("The unsafe_countdown function is written but not called.")
  print("=================================")