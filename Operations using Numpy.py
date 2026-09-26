
  import numpy as np
  data_type = [('name', '15'), ('class', int), ('height', float)]
  students_details = [('James', 5, 48.5), ('Nail', 6, 52.5),('Paul', 5, 42.10), ('Pit', 5, 40.11)]
    # create a structured array
    students = np.array(students_details, dtype=data_type)
    print("Original array:")
    print(students)
    print("Sort by height")
    print(np.sort(students, order='height'))
    import numpy as np
  
    a = np.arange(9, dtype=np.float_).reshape(3, 3)
    print('First array:')
    print(a)
    print('\n')
  
    b = np.array([10, 10, 10])
    print('Second array:')
    print(b)
    print('\n')
  
    print('Add the two arrays:')
    print(np.add(a, b))
    print('\n')
  
    print('Divide the two arrays:')
    print(np.divide(a, b))
    print('\n')