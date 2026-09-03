  # 02-list-sum.py
  # Topic: Sorted Check with Recursion, Sum of a List with Recursion

  def list sum(1st):
      if 1st == []:
          return 0
      return 1st[0] + list_sum(1st[1:])

  input("Recursive sum - add head to sum of tail until empty. Press Enter ")
  print("  list_sum([1, 2, 3]) =", list_sum([1, 2, 3]))
  print("  list_sum([4, 5, 6]) =", list_sum([4, 5, 6]))

  1st = [int(x) for x in input("Enter 4 numbers separated by spaces: ").split()]
  guess = input("What is the sum of " + str(1st) + "? ")
  input("list_sum adds head to list_sum(tail) until the list is empty. Press Enter ")
  print("  sum:", list_sum(1st), "  your guess:", guess)