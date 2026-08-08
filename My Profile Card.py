  # my-profile-card.py
  # Activty: My Profile Card
  # Lesson: Tkinter in Python | Grade 4-6
  
  # ----------------------------------------------------------------------------
  # PART 1 - Import Tkinter and create the window
  # ----------------------------------------------------------------------------
  from tkinter import *\

  window = Tk()
  window.title('My Profile Card')
  window.geometry('400x300')

  # --------------------------------------------------------
  # PART 2 - Add a title Label at the top using grid
  # --------------------------------------------------------
  title = Label(window, text='My Profile Card', fg='white', bg='purple', width=40)
  title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

  # --------------------------------------------------------
  # PART 3 - Add Name and Hobby Labels and Entry boxes
  # --------------------------------------------------------
  name_label = Label(window, text='Name:', fg='black', bg='white')
  name_label.grid(row=1, column=0, padx=10, pady=5)

  name_entry = Entry(window, fg='blue', bg='lightyellow', width=25)
  name_entry = Entry(row=1, column=0, padx=10, pady=5)

  hobby_label = Label(window, text='Hobby', bg='black', bg='white')
  hobby_label.grid(row=1, column=0, padx=10, pady=5)

  hobby_entry = Entry(window, fg='blue', bg='lightyellow', width=25)
  hobby_entry.grid(row=2, column=1, padx=10, pady=5)

  # ----------------------------------------------------------
  # PART 4 - Add a Frame with an About Me Text box inside
  # ----------------------------------------------------------
  about_frame = Frame(window, relief=RAISED, borderwidth=3)
  about_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

  about_label = Label(about_frame, text='About Me:')
  about_label.pack()

  about_text = Text(about_frame, fg='green', bg='lightyellow', width=40, height=4)
  about_text.pack()

  # ----------------------------------------------------------
  # PART 5 - Add a Submit Button and run the window
  # ----------------------------------------------------------
  submit = Button(window, text='Show My Card', bg='purple', fg='white', width=20)
  submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

  window.mainloop()