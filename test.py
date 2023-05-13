import tkinter as tk

# Create the master object
master = tk.Tk()

# Create a spinbox widget
spinbox_1 = tk.Spinbox(master, values=("Python", "Java", "C++"))

# And a label for it
label_1 = tk.Label(master, text="Language")

# Create another spinbox widget
spinbox_2 = tk.Spinbox(master, from_=1, to=3)

# And a label for it
label_2 = tk.Label(master, text="Value")

# Use the grid geometry manager to put the widgets in the respective position
label_1.grid(row=0, column=0)
spinbox_1.grid(row=0, column=1)

label_2.grid(row=1, column=0)
spinbox_2.grid(row=1, column=1)

# The application mainloop
tk.mainloop()
