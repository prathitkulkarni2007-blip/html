  # 02-total-profit.py
  # Topic: Profit accumulation
  
  def total_profit(n):
      prices = [1, n, 1, n, 1]
      profit = 0
      for i in range(1, len(prices)):
          if prices[i] > prices[i - 1]:
              profit += prices[i] - prices[i - 1]
      return profit

 input("total_profit(n) sums every upswing in prices [1, n, 1, n, 1.  Press Enter ")
 print("  total_profit(4) =", total_profit(4))
 print("  total_profit(5) =", total_profit(5))
 n = int(input("Enter n (try 6 or 7): "))
 guess = input("What is total__profit(" + str(n) + ")? ")
 input("add every positive step — two peaks each contribute n-1.  Press Enter ")
 print("  total__profit(" + str(n) + ") =", total_profit(n), "  your guess:", guess)