  # =========================================
  # MY WEATHER REPORTER
  # File: my-weather-reporter.py
  # =========================================


  # PART 1 - USER INPUT
  city = input("Enter your city name: ")
  temp = float(input("Enter your city name: ")
               

  # PART 2 - if STATEMENT
  if temp > 35:
      print("Warning: It is very hot today!")


  # PART 3 - if-else
  if temp > 25:
      print("Great day to go outside!")
  else:
      print("Grab a jacket before you go out!")


  # PART 4 - if-elif-else
  if temp > 35:
      print("Weather: Scorching Hot")
  elif temp > 25:
      print("Weather: Warm and Sunny")
  elif temp > 15:
      print("Weather: Cool and Breezy")
  else:
      print("Weather: Cold - stay warm!")


  # PART 5 - datetime MODULE
  import datetime
  import calendar

  now = datetime.datetime.now()
  print("City:", city)
  print("Time now:", now)

  print(calendar.calendar(now.year))