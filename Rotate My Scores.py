 # ===============================
 # ROTATE MY SCORES
 # ===============================
 # Topics:
 # Two-pointer swap | Reverse in groups
 # Left rotate by 1 | Left rotate by n
 # Leaders in an array
 
 print("================================")
 print("ROTATE MY SCORES")
 print("================================")


 # -------------------------------------------------
 # PART 1 - TWO_POINTER SWAP
 # -------------------------------------------------

 scores = [10, 20, 30, 40, 50]

 print("
 PART 1: Two-Pointer Swap")
 print("Original Scores:", scores)

 start = 0
 end = len(scores) - 1

 while start < end:
     scores[start], scores[end] = scores[end], scores[start]
     start = start + 1
     end = end - 1

 print("Reversed Scores:", scores)


 # -------------------------------------------------
 # PART 2 - REVERSE IN GROUPS
 # -------------------------------------------------

 scores = [1, 2, 3, 4, 5, 6, 7, 8]
 group_size = 3

 print("
 PART 2: Reverse in Groups")
 print("Original Scores:", scores)
 print("Group Size:", group_size)

 i = 0

 while i < len(scores):
     start = i
     end = min(i + group_size - 1, len(scores) - 1)

     while start < end:
         scores[start], scores[end] = scores[end], scores[start]
         start = start + 1
         end = end - 1

     i = i + group__size

 print("Scores After Group Reverse:", scores)


 # -------------------------------------------------
 # PART 3 - LEFT ROTATE BY 1
 # -------------------------------------------------

 scores = [10, 20, 30, 40, 50]

 print("
 PART 3: Left Rotate by 1")
 print("Original Scores:", scores)

 first_score = scores[0]

 for i in range(len(scores) - 1):
     scores[i] = scores[i + 1]

 scores[-1] = first_score

 print("After Left Rotate by 1:", scores)


 # -------------------------------------------------
 # PART 4 - LEFT ROTATE BY n
 # -------------------------------------------------

 scores = [10, 20, 30, 40, 50, 60]
 n = 2

 print("
 PART 4: Left Rotate by n")
 print("Original Scores:", scores)
 print("Rotate By:", n)

 n = n % len(scores)

 for rotation in range(n):
     first_score = scores[0]

     for i in range(len(scores) - 1):
         scores[i] = scores[i + 1]

     scores[-1] = first_score

 print("After Left Rotate by n:", scores)


 # -------------------------------------------------
 # PART 5 - LEADERS IN AN ARRAY
 # -------------------------------------------------

 scores = [16, 17, 4, 3, 5, 2]
 leaders = []

 print("
 PART 5: Leaders in an Array")
 print("Scores:", scores)

 max_from_right = scores[-1]
 leaders.append(max_from_right)

 i = len(scores) - 2

 while i >= 0:
     if scores[i] > max_from_right:
        max_from_right = scores[i]
        leaders.append(scores[i])

     i = i - 1

 leaders.reverse()

 print("Leaders:", leaders)


 # FINAL SUMMARY

 print("
 ===============================")
 print("ROTATE MY SCORES SUMMARY")
 print("===============================")
 print("Two-pointer swap reversed the list.")
 print("Reverse in groups changed fixed-size score groups.")
 print("Left rotate by 1 moved the first score to the end.")
 print("Left rotate by n repeated the left rotation multiple times.")
 print("Leaders are scores greater than all scores on their right.")
 print("===============================")