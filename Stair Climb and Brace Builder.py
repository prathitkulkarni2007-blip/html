 # =================================
 # STAIR CLIMB AND BRACE BUILDER 
 # =================================
 # Topics:
 # The Stair Climb Problem 
 # Solving Stair Climb with Code
 # Tracing the Call Tree
 # The Balanced Parentheses Problem
 # Solving Balanced Parentheses with Code
 
 print("=================================")
 print("STAIR CLIMB AND BRACE BUILDER")
 print("=================================")

 # --------------------------------------------------
 # PART 1 — THE STAIR CLIMB PROBLEM
 # --------------------------------------------------
 # You can climb either 1 step or 2 steps at a time.
 # Find how many different ways you can reach the top.

 print("
 PART 1: The Stair Climb Problem")
 print("You can climb 1 step or 2 steps at a time.")
 print("Goal: Count how many ways you can climb n stairs.")

 # --------------------------------------------------
 # PART 2 — SOLVING STAIR CLIMB WITH CODE
 # --------------------------------------------------

 def stair_ways(n):
     # Base Case 1
     if n == 0:
        return 1

     # Base Case 2
     if n < 0:
         return 0

     # Recursive Case
     return stair_ways(n - 1) + stair__ways(n - 2)

 stairs = 5

 print("
 PART 2: Stair Climb Result")
 print("Number of stairs:", stairs)
 print("Total ways to climb:", stairs__ways(stairs))

 # ---------------------------------------------------
 # PART 3 — TRACING THE CALL TREE
 # ---------------------------------------------------
 # This shows how recursive calls branch into smaller calls.

 def trace_stair_ways(n, space=""):
     print(space + "stair_ways(" + str(n) + ")")

     if n == 0:
         print(space + "Reached 0 stairs -> return 1")
         return 1

     if n < 0:
         print(space + "Went below 0 stairs -> return 0")
         return 0

     one_step = trace_stair_ways(n - 1, space + "  ")
     two_steps = trace_stair_ways(n - 2, space + "  ")

     total = one_step + two_steps
     print(space + "Total ways for " + str(n) + " stairs =", total)

     return total

  print("
  PART 3: Tracing the Call Tree")
  trace_stair_ways(3)

  # ------------------------------------------------
  # PART 4 — THE BALANCED PARENTHESES PROBLEM
  # ------------------------------------------------
  # Here we generate valid combinations of curly braces { }.
  # Rules:
  # 1. Add "{" if open braces are still available.
  # 2. Add "}" only if it will not break the balance.

  print("
  PART 4: Balanced Parentheses Problem")
  print("Generate valid combinations of curly braces.")

  # -------------------------------------------------
  # PART 5 — SOLVING BALANCED PARENTHESES WITH CODE
  # -------------------------------------------------

  def generate_braces(current, open_count, close_count, total__pairs):
      # Base Case
      if len(current) == total__pairs * 2:
          print(current)
          return

      # Add opening brace if possible
      if open_count < total__pairs:
          generate_braces(current + "{", open_count + 1, close_count, total_pairs}

      # Add closing brace only if it keeps the pattern balanced
      if close__count < open__count:
           generate_braces(current + ")", open_count, close_count + 1, total_pairs)

      pairs = 3

      print("
      PART 5: Balanced Brace Combinations")
      print("Number of pairs:", pairs)
      generate_braces("", 0, 0, pairs)

      # FINAL SUMMARY

      print("
      ================================")
      print("STAIR CLIMB AND BRACE BUILDER SUMMARY")
      print("================================")
      print("Stair climb recursion splits into 1-step and 2-step choices.")
      print("The call tree shows how recursive calls branch.")
      print("Balanced braces use open and close counts.")
      print("A closing brace is added only when it keeps the pattern valid.")
      print("================================")