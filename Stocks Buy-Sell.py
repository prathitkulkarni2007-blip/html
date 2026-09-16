 # 01-max-profit.py
 # Topic: Stocks buy-sell
 
 def max_profit(n):
     prices = list(range(n, 0, -1)) + list(range(1, n + 1))
     min_price, profit = prices[0], 0
     for p in prices[1:]:
         min_price = min(min_price, p)
         profit = max(profit, p - min_price)
     return profit

 input("max_profit(n) finds the best single buy-sell in prices [n..1, 1..n].   Press Enter")
 print("   max_profit(4) =", max_profit(4))
 print("   max_profit(5) =", max_profit(5))
 n = int(input("Enter n (try 6 or 7): "))
 guess = input("What is max_profit(" + str(n) + ")? ")
 input("track min price so far — sell when the gap beats the current best.  Press Enter ")
 print("  max_profit(" + str(n) + ") =", max_profit(n), "  your guess:", guess)