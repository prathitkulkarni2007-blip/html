  # game-starts-analyser.py
  # Activity: Gaming Leaderboard Analyser
  # Lesson: Introduction to Pandas
  
  import pandas as pd 

  # PART 1 - Create a Pandas Series of top player scores
  print('--- PART 1: Pandas Series ---')
  scores = [98500, 87200, 76400, 65100, 54800]
  players = pd.Series(scores, index=['NightWolf', 'StarBlaze', 'PixelKing', 'CyberFox', 'IronStorm'])
  print(players)
  
  # PART 2 - Create a DataFrame of gaming stats
  print()
  print('--- PART 2: Pandas DataFrame ---')
  data = {
    'Player': ['NightWolf', 'StarBlaze', 'PixelKing', 'CyberFox', 'IronStorm'],
    'Level':  [42, 38, 35, 30, 27],
    'Score':  [98500, 87200, 76400, 65100, 54800],
    'Wins':   [210, 185, 162, 140, 118]
  }
  df = pd.DataFrame(data)
  print(df)

  # PART 3 - Access rows using .loc
  print()
  print('--- PART 3: Accessing Rows ---')
  print('Row 0 (top player):')
  print(df.loc[0])
  print()
  print('Rows 2 and 3:')
  print(df.loc[2:3])

  # PART 4 - Loaf leaderboard.csv and view the data
  print()
  print('--- PART 4: Reading a CSV File ---')
  full_df = pd.read_csv('leaderboard.csv')
  print('First 5 rows (head):')
  print(full_df.head())
  print()
  print('Last 3 rows (tail):')
  print(full_df.tail(3))
  print()
  print('Dataset info:')
  print(full_df.info())

  # PART 5 - Clean the data
  print()
  print('--- PART 5: Cleaning Data ---')
  print('Rows with missing values removed (dropna):')
  clean_df = full_df.dropna()
  print(clean_df.to_string())
  print()
  print('Missing values filled with 0 (fillna):')
  filled_df = full_df.fillna(0)
  print(filled_df.to_string())