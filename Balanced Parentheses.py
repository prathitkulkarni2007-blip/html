  # 03-balanced-parens.py
  # Topic: The Balanced Parentheses Problem, Solving Balanced Parentheses with Code 
  
  def count _paren(n, l=0, r=0):
      if l == n and r == n:
          return 1
      total = 0
      if l > r:
          total += count__paren(n, l, r + 1)
      if l < n:
          total += count__paren(n, l + 1, r)
      return total

  input("count_paren counts every valid {} sequence — returns 1 at each valid end. Press Enter ")
  print(" count_paren(1) =", count_paren(1))
  print(" count_paren(2) =", count_paren(2))

  n = int(input("Enter number of pairs (try 3 or 4): "))
  guess = input("What is count__paren(" + str(n) + ")? ")
  input("l>r close l<n opens —— adds 1 at every valid ending. Press Enter")
  print("  count__paren(" + str(n) + ") =", count_paren(n), " your guess:", guess)