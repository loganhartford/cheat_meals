import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a Tkinter window
root = tk.Tk()
root.geometry("500x300")

# Create a Figure object and add a subplot
fig, ax = plt.subplots(figsize=(8, 5))

# Nutrient labels
nutrients = ["Protein", "Fat", "Carbohydrates", "Fiber"]

# Recommended daily values (DV)
dv_values = [50, 70, 300, 25]

# Actual values for the meal
actual_values = [35, 40, 250, 20]

# Bar width
width = 0.35

# Create the double bar graph
ax.bar(range(len(nutrients)), dv_values, width, label="Recommended DV")
ax.bar([i + width for i in range(len(nutrients))], actual_values, width, label="Actual")

# Set the x-axis tick positions and labels
ax.set_xticks([i + width / 2 for i in range(len(nutrients))])
ax.set_xticklabels(nutrients)

# Set the y-axis label
ax.set_ylabel("Amount")

# Add a legend
ax.legend()

# Create a canvas and add the figure to it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# Add the canvas to the Tkinter window
canvas.get_tk_widget().grid(row=0, column=0)

# Run the Tkinter event loop
root.mainloop()
