  # 02-left-rotate.py
  # Topic: Left rotate by 1, Left rotate by n
  
  def left_rotate(n):
      arr = [1, 2, 3, 4, 5]
      n = n % len(arr)
      return arr[n:] + arr[:n]

  input("left rotate(n) shifts [1,2,3,4,5] left by n positions.  Press Enter ")
  print("  left_rotate(1) =", left_rotate(1))
  print("  left_rotate(2) =", left_rotate(2))
  n = int(input("Rotate by how many? (try 3 or 4): "))
  guess =  input("What is left_rotate(" + str(n) + ")? ")
  input("slice from index n to end, then attach the first n elements. Press Enter ")\
  print("  left_rotate(" + str(n) + ") =", left_rotate(n), " your guess:", guess)