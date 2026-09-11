 # ==============================
 # KEYPAD WORD GENERATOR
 # ==============================
 # Topics:
 # Thinking Recursively | Tower of Hanoi
 # Phone Keypad | Recursion Trees
 # How Problems Grow
 
 print("===============================")
 print("KEYPAD WORD GENERATOR")
 print("===============================")


 # --------------------------------------------------
 # PART 1 — THINKING RECURSIVELY
 # --------------------------------------------------

 print("\nPART 1: Thinking Recursively")
 print("A recursive solution breaks one big problem into smaller versions of the same problem.")
 print("Each recursive function needs a base case and a recursive case.")


 # --------------------------------------------------
 # PART 2 — TOWER OF HANOI
 # --------------------------------------------------

 def tower__of__hanoi(disks, source, helper, destination):
     # Base Case
     if disks == 1:
         print("Move disk 1 from", source, "to", destination)
         return

     # Step 1: Move smaller disks to helper
     tower__of__hanoi(disks - 1, source, destination, helper)

     # Step 2: Move largest disk to destination
     print("Move disk", disks, "from", source, "to", destination)

     # Step 3: Move smaller disks to helper to destination
     tower__of__hanoi(disks - 1, helper, source, destination)


  print("\nPART 2: Tower of Hanoi")
  tower__of__hanoi(3, "A", "B", "C")


  # ---------------------------------------------------
  # PART 3 —— PHONE KEYPAD
  # ---------------------------------------------------

  keypad = {
      "2": ["a", "b", "c"],
      "3": ["d", "e", "f"],
      "4": ["g", "h", "i"],
      "5": ["j", "k", "l"],
      "6": ["m", "n", "o"],
      "7": ["p", "q", "r", "s"],
      "8": ["t", "u", "v"],
      "9": ["w", "x", "y", "z"]
  }


 # ---------------------------------------------------
 # PART 4 —— KEYPAD WORD GENERATOR
 # ---------------------------------------------------

 def generate_words(digits, current_word):
     # Base Case
     if len(digits) == 0:
         print(current_word)
         return

     first_digit = digits[0]
     remaining__ digits = digits[1:]

     for letter in keypad[first_digit]:
         generate_words(remaining_digits, current_word + letter)


 print("\nPART 4: Phone Keypad Combinations")
 number = "23"

 print("Digits:", number)
 print("Possible words:")
 generate_words(number, "")


 # ---------------------------------------------
 # PART 5 — RECURSION TREE AND PROBLEM GROWTH
 # ---------------------------------------------

 def show_recursion_tree(digits, current_word, level):
     indent = "  " * level

     if len(digits) == 0:
         print(indent + "Word completed: " + current_word)
         return

     first_digit = digits[0]
     remaining_digits = digits[1:]

     print(indent + "Current word: " + current__word + " | Next digit: " + first_digit)

     for letter in keypad[first_digit]:
         show_recursion_tree(remaining_digits, current_word + letter, level + 1)


 print("\nPART 5: Recursion Tree")
 show_recursion_tree("23", "", 0)


 # FINAL SUMMARY

 print("\n==============================")
 print("KEYPAD WORD GENERATOR SUMMARY")
 print("================================")
 print("Thinking recursively means solving a smaller version of the same problem.")
 print("Tower of Hanoi uses recursion to move disks step by step.")
 print("Phone keypad recursion builds words one letter at a time.")
 print("A recursion tree shows how calls branch and grow.")
 print("More digits create more combinations.")
 print("===============================")