  # NOTEBOOK MERGER 
  # Topics: with open() | sprit() | os.path.exists() | os.remove() | File Merge
  
  import os

  # PART 1 -- Read with Auto-Close
  print("=== Science Notes ===")
  with open("science-notes.txt", "r") as f:
      for line in f:
          print(line.strip())
 print()

 # PART 2 -- Count Words in Each Line
 print("=== Word Count ===")
 with open("maths-notes.txt", "r") as f:
     for line in f:
         words = line.split()
         print(len(words), "words ->", line.strip())
 print()

 # PART 3 -- Check and Merge
 print("=== Merging Notes ===")
 if os.path.exists("all-notes.txt"):
     print("all-notes.txt already exists - overwriting")
 else:
     print("all-notes.txt not found - creating now")

 content = ""
 with open("science-notes.txt", "r") as f:
     content += "--- science-notes.txt ---\n"
     content += f.read() + "\n"
 with open("maths-notes.txt", "r") as f:
     content += "--- maths-notes.txt ---\n"
     content += f.read() + "\n"
 with open("all-notes.txt", "w") as out:
     out.write(content)
 print("Saved to all-notes.txt")
 print()

 # PART 4 -- Delete the Merged File
 if os.path.exists("all-notes.txt"):
     os.remove("all-notes.txt")
     print("all-notes.txt deleted.")
 else:
     print("all-notes.txt does not exist.")