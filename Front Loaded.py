  # 02-max-front.py
  # Topic: The Drag of Negatives, Max-So-Far Tracker

  def max_front(n):
      arr = [1]*n + [-1]
      current = best = arr[0]
      for x in arr[1:]:
          if current < 0: current = x
          else: current = current + x
          if current > best: best = current 
      return best

  input("max_front(n) finds the max subarray sum in [1, 1, ..., 1, -1]. Press Enter ")
  print("  max_front(3) =", max_front(3))
  print("  max_front(4) =", max_front(4))
  n = int(input("Enter n (try 5 or 6): "))
  guess = input("What is max_front(" + str(n) + ")? ")
  input("best locks in n ones —— the last -1 drags sum down but best holds. Press Enter ")
  print("  max_front(" + str(n) + ") =", max_front(n), "  your guess:", guess)