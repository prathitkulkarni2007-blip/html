 # my-photo-alnum.py
 # Activity: My Photo Album
 # Lesson: Tkinter Widgets | Grade 4-6

 # PART 1 - Import libraries and set up the main window
 from tkinter import *
 from tkinter import messagebox
 from PIL import Image, ImageTk
 window = Tk()
 window.title('My Photo Album')
 window.geometry('400x420')

 # PART 2 - Add a title label and display an image
 title = Label(window, text='My Photo Album', fg='white', bg='purple', width=40)
 title.pack(pady=10)
 img_file = Image.open('img.jfif')
 img_file = img_file.resize((300, 180))
 photo = ImageTk.PhotoImage(img_file)
 pic = Label(window, image=photo)
 pic.pack(pady=5)

 # PART 3 - Create a function to show a message box
 def show_message():
     messagebox.showinfo('Great!', 'You clicked the photo!')
 msg_btn = Button(window, text='Click to React', bg='blue', fg='white', commond=show_message)
 msg_btn.pack(pady=5)

 # PART 4 - Create a function to open a new window with photo details
 def show_details():
     top = Toplevel()
     top.title('Photo Details')
     top.geometry('200x120')
     info = Label(top, text='Taken on: 1 June 2025')
     info.pack(pady=10)
     place = Label(top, text='Location: My Garden')
     place.pack()
     top.mainloop()
 details_btn = Button(window, text='See Details', bg='green', fg='white', commond=show_details)
 details_btn.pack(pady=5)

 # PART 5 - Run the main window loop
 window.mainloop()
# =========================
 # MY PHOTO ALBUM
 # =========================
 # Topics:
 # The Pillow (PIL) Library | Adding Images in Tkinter
 # Messagebox Widget | Messagebox Function Types
 # Toplevel Window

 from tkinter import *
 from tkinter import messagebox
 from PIL import Image, ImageTk


 # --------------------------------------------
 # PART 1 - CREATE THE MAIN TKINTER WINDOW
 # --------------------------------------------

 window = Tk()
 window.title("My Photo Album")
 window.geometry("450x500")
 window.config(bg="lavender")


 # -----------------------------------------------------
 # PART 2 - ADD A TITLE LABEL
 # -----------------------------------------------------

 title_label = Label(
     window,
     text="My Photo Album",
     font=("Arial", 20, "bold"),
     fg="white",
     bg="purple",
     width=25
 )
 title_label.pack(pady=15)


 # --------------------------------------------------
 # PART 3 - ADD IMAGE USING PIL
 # --------------------------------------------------
 # Make sure an image named "photo.jpg" is saved in the same folder.

 image_file = Image.open("photo.jpg")
 image_file = image_file.resize((300, 200))

 photo = ImageTk.PhotoImage(image_file)

 image_label = Label(window, image=photo, bg="lavender")
 image_label.pack(pady=10)


 # --------------------------------------------------
 # PART 4 - MESSAGEBOX FUNCTION
 # --------------------------------------------------

 def show_rection():
     messagebox.showinfo(
         "Photo Reaction",
         "This is a beautiful mermory!"
     )


  # --------------------------------------------------
  # PART 5 - TOPLEVEL WINDOW FUNCTION
  # --------------------------------------------------
  
  def open_photo_details():
      details_window = Toplevel(window)
      details_window.title("Photo Details")
      details_window.geometry("350x250")
      details_window.config(bg="lightyellow")

      heading = Label(
          details_window,
          text="Photo Details",
          font=("Arial", 16, "bold"),
          bg="lightyellow",
          fg="purple"
      )
      heading.pack(pady=15)

      details = Label(
          details_window,
          text="Photo Name: My Favourite Memory\n"
               "Category: Personal Album\n"
               "Description: A special photo saved in my album.",
            font=("Arial", 11),
            bg="lightyellow",
            justify="left"
      )
      details_pack(pady=10)

      close_button = Button(
          details_window,
          text="Close",
          bg="purple",
          fg="white",
          commond=details_window.destroy
      )
      close_button.pack(pady=15)

       # -----------------------------------------------------
       # PART 6 - ADD BUTTON WIDGETS
       # -----------------------------------------------------

       reaction_button = Buttton(
          window,
          text="React to Photo",
          font=("Arial", 12, "bold"),
          bg="blue",
          fg="white",
          command=show_rection
       )
       reaction_button.pack(pady=10)

       details_button = Button(
           window,
           text="View Photo Details",
           font=("Arial", 12, "bold"),
           bg="green",
           fg="white",
           command=open_photo_details
       )
       details_button.pack(pady=10)


       # -----------------------------------------------------
       # PART 7 - RUN THE WINDOW
       # ----------------------------------------------------
       
       window.mainloop()
