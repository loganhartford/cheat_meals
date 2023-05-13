import matplotlib.pyplot as plt
import numpy as np

# Define the daily recommended value for each nutrient
# These values will depend on the nutrient and the age/gender of the individual
# For this example, we'll use some arbitrary values
daily_values = {
    "protein": 50,
    "fat": 65,
    "carbs": 300,
    "fiber": 25,
    "sugar": 50,
    "sodium": 2300,
}

# Define the nutrient values for the food
# These values would come from the nutrition API or database
# For this example, we'll use some arbitrary values
nutrient_values = {
    "protein": 30,
    "fat": 15,
    "carbs": 60,
    "fiber": 10,
    "sugar": 20,
    "sodium": 800,
}

# Calculate the percentage of daily value for each nutrient
percent_daily_values = {
    k: v / daily_values[k] * 100 for k, v in nutrient_values.items()
}

# Define the colors for each nutrient
# These could be customized depending on the application
colors = {
    "protein": "green",
    "fat": "red",
    "carbs": "orange",
    "fiber": "brown",
    "sugar": "yellow",
    "sodium": "gray",
}

# Create the horizontal bar chart
fig, ax = plt.subplots(figsize=(8, 4))
y_pos = np.arange(len(percent_daily_values))
bars = ax.barh(y_pos, percent_daily_values.values(), align="center")
ax.set_yticks(y_pos)
ax.set_yticklabels(percent_daily_values.keys())
ax.set_xlabel("Percentage of Daily Value")
ax.set_xlim([0, 100])

# Set the color of each bar based on the nutrient
for i, nutrient in enumerate(percent_daily_values.keys()):
    bars[i].set_color(colors[nutrient])

# Add the percentage values to the bars
for i, v in enumerate(percent_daily_values.values()):
    ax.text(v + 2, i, f"{v:.0f}%", color=colors[list(percent_daily_values.keys())[i]])

plt.show()
