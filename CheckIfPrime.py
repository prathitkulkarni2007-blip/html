  # Program to check if given number is prime or not

  from math import sqrt

  number = int(input("Enter your number : "))
  print("\n")

  # If given number is greater than 1
  if number > 1:

      # check if number is divisible from 2 to number/2
      for i in range(2, int(sqrt(number))+1):

          # if divisible by any number it is a non prime number
          if (number % i)  == 0:
              print(number, "is not a prime number")
              break
      else:
          print(number, "is a prime number")

    else:
        print(number, "is not a prime number")