  # 01-reverse.py
  # Topic: Two–pointer swap, Reverse in groups
 
  def reverse(n):
      arr, i, j = list(range(1, n + 1)), 0, n - 1
      while i < j:
         arr[i], arr[j] = arr[j], arr[i]
         i += 1; j -= 1
      return arr

  input("reverse(n) builds [1..n] and flips it end-to-end using two pointers. Press Enter ")
  print(" reverse(4) =", reverse(4))
  print(" reverse(5) =", reverse(5))
  n = int(input("Enter list size (try 6 or 7): "))
  guess = input("What is reverse(" + str(n) + ")? ")
  input("left and right swap and move inward until they meet in the middle.  Press Enter ")
  print(" reverse(" + str(n) + ") =", reverse(n), "  your guess:", guess)