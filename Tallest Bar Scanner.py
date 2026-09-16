 # ===================================
 # TALLEST BAR SCANNER
 # ===================================
 # Topics:
 # Stocks buy-sell | Profit accumulation
 # Left tallest bars | Right tallest bars
 # Rainwater trapped
 
 print("================================")
 print("TALLEST BAR SCANNER")
 print("================================")


 # ---------------------------------------------------
 # PART 1 - STOCK BUY-SELL
 # ---------------------------------------------------

 prices = [100, 180, 260, 310, 40, 535, 695]

 print("\nPART 1: Stocks Buy-Sell")
 print("Stock Prices:", prices)

 profit = 0

 for i in range(1, len(prices)):
     if prices[i] > prices[i - 1]:
         gain = prices[i] - prices[i - 1]
         profit = profit + gain
         print("Buy at", prices[i - 1], "Sell at", prices[i], "Gain:", gain)

 print("Maximum Profit:", profit)


 # -----------------------------------------------
 # PART 2 - PROFIT ACCUMULATION
 # -----------------------------------------------

 print("\nPART 2: Profit Accumulation")

 total_profit = 0

 for i in range(1, len(prices)):
     daily_difference = prices[i] - prices[i - 1]

     if daily_difference > 0:
         total_profit = total_profit + daily_difference
         print("Added profit:", daily_difference)

 print("Total Accumulated Profit:", total_profit)


 # ---------------------------------------------------
 # PART 3 - LEFT TALLEST BARS
 # ---------------------------------------------------

 heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
 n = len(heights)

 left_tallest = [0] * n
 left_tallest[0] = heights[0]

 for i in range(1, n):
     left_tallest[i] = max(left_tallest[i - 1], heights[i])

 print("\nPART 3: Left Tallest Bars")
 print("Heights:      ", heights)
 print("Left Tallest: ", left_tallest)


  # ---------------------------------------------------
  # PART 4 - RIGHT TALLEST BAR
  # ---------------------------------------------------
  
  right_tallest = [0] * n
  right_tallest[n - 1] = height[n - 1]

  for i in range(n - 2, -1, -1):
      right_tallest[i] = max(right_tallest[i - 1], heights[i])

  print("\nPART 4: Right Tallest Bars")
  print("Heights:       ", heights)
  print("Right Tallest: ", right_tallest)


  # ---------------------------------------------------
  # PART 5 - RAINWATER TRAPPED
  # ---------------------------------------------------

  water = 0

  for i in range(n):
      small_bar = min(left_tallest[i], right_tallest[i])
      trapped = small_bar - heights[i]
      water = water + trapped

  print("\nPART 5: Rainwater Trapped")
  print("Total Rainwater Trapped:", water)


  # FINAL SUMMARY
  
  print("\n===============================")
  print("TALLEST BAR SCANNER SUMMARY")
  print("===============================")
  print("Stock profit was calculated by adding every positive price difference.")
  print("Left tallest bars store the highest bar seen from the left side.")
  print("Right tallest bars store the highest bar seen from the right side.")
  print("Rainwater is calculated using the smaller value from left and right tallest bars.")
  print("===============================")