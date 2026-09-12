 # Function to find the number and print it. 
 def print2largest(a, a_size):
     largest = secondLargest = -2147483648
     for i in range(a_size):

         # If the current element of the array is greater than our current largest number, then replace
              if (a[i] > largest):


                  secondLargest = largest
                  largest = a[i]


         # If current element is less than current largest but greater than second largest then replace the number
         elif (a[i] > secondLargest and a[i] != largest):
             secondLargest = a[i]


         print(secondLargest)


    a = [1,2,3,4,5,6,7,8,9]
    a_size = len(a)
    print2largest(a, a_size)