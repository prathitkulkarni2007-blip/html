  # 02-steps-at-scale.py
  # Topic: Time Complexity — how steps grow as n gets bigger
  # Double Loop at n = 4 took 10 steps. Watch what happens as n grows.
  
  input("Double Loop at n = 4 took 10 steps. Watch it grow. Press Enter ")
  for n in [10, 100, 1000]:
      input("n = " + str(n) + "  Press Enter")
      print(" steps =", n * (n + 1) // 2)