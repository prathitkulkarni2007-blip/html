 # 03-group-reverse.py
 # Topic: Reverse in groups

 def group_reverse(n):
     arr = [1, 2, 3, 4, 5, 6]
     for i in range(0, 6, n):
         arr[i:i+n] = arr[i:i+n][::-1]
     return arr

 input("group_reverse(n) reverses [1,2,3,4,5,6] in chunks of n.  Press Enter")
 print("  group_reverse(2) =", group_reverse(2))
 print("  group_reverse(3) =", group_reverse(3))
 n = int(input("Group size (try 1 or 6): "))
 guess = input("What is group_reverse(" + str(n) + ")? ")
 input("each chunk of n elements is flipped in place. Press Enter ")
 print("  group__reverse(" + str(n) + ") =", group_reverse(n)," your guess:", guess)