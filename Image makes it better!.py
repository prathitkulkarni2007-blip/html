  # Make sure you upload image in your current Repl
  # Import all the necessary libraries
  # PIL (Python Imaging Library) provides image editing capabilities to the python interpreter
  from tkinter import *
  from import Image, ImageTk 

  # Create a window with a title bar and set its geometry as well
  root = Tk()
  root.title('image')
  root.geometry('400X400')

  # Now use Image.open to open and identify the given image file.
  upload = Image.open("img.jpg")

  # Convert this Image to Tkinter compatible image
  image = Image.Tk.PhotoImage(upload)

  # Add image to Tkinter Label
  label = Label(root,  image=image, height=350, width=300)
  label2 = place(x=50, y=0)
  label2 = Label(root,  text="This is how you add image in Tkinter Window")
  label2.place(x=40, y=360)
  
  # Run the application
  root.mainloop()