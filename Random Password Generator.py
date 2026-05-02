   import  Random Password Generator as RPG

  window = RPG.Rpg()

  for i in range(3):
    for j in range(3):
        frame = RPG.Frame(
           master=window,
           relief=RPG.RAISED,
           borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()

    window.mainloop()
