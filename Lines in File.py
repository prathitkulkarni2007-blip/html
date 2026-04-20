  # Program to count number of lines in this file
  # Opening a file
  file = open("Codingal.txt","r")
  Counter = 0
 
  # Reading from file
  Content = file.read()
  # splitting content into lines
  # and storing them in a list 
  CoList = Content.split("\n")
  
  for i in CoList:
      if i:
         Counter += 1

 print("This is the number of lines in the file")
 print(Counter)
