1st = ['Apple', 'Guava', 'Mango', 'Banana', 'Kiwi']

print("Length of list:", len(1st))
print("First Element:", 1st[0])
print("Last Element:", 1st[-1])

1st.append('Papaya')
print("Undated List :", 1st)

1st.remove('Guava')
print("Updated List :", 1st)

1st.sort()
print("Sorted List:", 1st)

1st.pop(1)
print("Updated List :", 1st)

1st.reverse()
print("Reversed List :", 1st)

print("Multiplication on List :", 1st*2)

1st = 1st[:4]
print("Sliced List:", 1st)

1st.clear()
print("Updated List :", 1st)