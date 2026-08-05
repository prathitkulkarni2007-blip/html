  # NOTES CLEANER
  # Topics: read(n)  | readlines() | Loop Through File | Filter Lines | Copy Odd Lines
  
  # PART 1 -- Sneak Peek 
  n = int(input("How many characters to preview? "))
  file = open("class-notes.txt", "r")
  print(file.read(n))
  file.close()
  print()

  # PART 2 -- All Lines as a List
  file = open("class-notes.txt", "r")
  lines = file.readlines()
  file.close()
  print("Total lines:", len(lines))
  for i in range(len(lines)):
      print(i + 1, "->", lines[i].strip())
  print()

   # PART 3 -- Filter Lines
   word = input("Skip lines starting with: ")
   file = open("class-notes.txt", "r")
   for line in file:
       if line.startswith(word):
           print("skip ->", line.strip())
       else:
           print("keep ->", line.strip())
   file.close()
   print()

   # PART 4 -- Copy Odd Lines to New File
   file = open("class-notes.txt", "r")
   lines = file.readlines()
   file.close()
   out = open("odd-lines.txt", "w")
   for i in range(0, len(lines), 2):
       out.write(lines[i])
    out.close()
    print("Odd lines saved to odd-lines.txt")