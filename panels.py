import customtkinter as ctk
from imgage_widgets import StaticImage
from settings import *
from data import get_cheat_meals
from errors import ErrorMesage
import json
from PIL import Image
from widgets import IconAndText, DisplayTextBox, MacroWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
import textwrap
import webbrowser

DEV_VERSTION = False  # Disalbes some app features for faster development
if DEV_VERSTION:
    import pandas as pd


class LogoPanel(ctk.CTkFrame):
    """Fills the entire panel with a logo image"""

    def __init__(self, parent, logo_img, col, row):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col,
            row=row,
            sticky="nsew",
            pady=(HEADER_PADY_TOP - 7, 0),
            padx=(5, 0),
        )

        # Layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        # Widgets
        StaticImage(self, logo_img, "white", 0, 0)


class UserInputPanel(ctk.CTkFrame):
    """This panel includes all of the user input elements."""

    def __init__(self, parent, cheat_score, meal_data, col, row, colspan):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col,
            row=row,
            columnspan=colspan,
            sticky="nsew",
            pady=(HEADER_PADY_TOP, HEADER_PADY_BOT),
            padx=(0, 10),
        )
        self.parent = parent

        # Fonts
        self.entry_font = ctk.CTkFont(family=FAMILY, size=16)
        self.dropdown_font = ctk.CTkFont(family=FAMILY, size=14)
        self.cheat_score_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")
        self.button_font = ctk.CTkFont(family=FAMILY, size=18, weight="bold")

        # Data
        self.meal_data = meal_data
        self.cheat_score = cheat_score
        self.cheat_score_display = ctk.StringVar()
        self.update_display()
        self.cheat_score.trace("w", self.update_display)

        # Layout
        self.columnconfigure((0, 1), weight=3, uniform="a")
        self.columnconfigure((2, 3, 4), weight=2, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")

        # Widgets
        # Address input
        self.address_entry = ctk.CTkEntry(
            master=self,
            text_color=TEXT_COLOR,
            fg_color=BG_COLOR,
            font=self.entry_font,
            placeholder_text="Street Address",
            border_color=BORDER_COLOR,
            border_width=BORDER_WIDTH,
        )
        self.address_entry.grid(
            column=0, row=0, columnspan=2, sticky="nsew", pady=(0, 2.5), padx=5
        )
        self.city_entry = ctk.CTkEntry(
            master=self,
            text_color=TEXT_COLOR,
            fg_color=BG_COLOR,
            font=self.entry_font,
            placeholder_text="City",
            border_color=BORDER_COLOR,
            border_width=BORDER_WIDTH,
        )
        self.city_entry.grid(
            column=0, row=1, sticky="nsew", pady=(2.5, 0), padx=(5, 2.5)
        )
        self.province_entry = ctk.CTkEntry(
            master=self,
            text_color=TEXT_COLOR,
            fg_color=BG_COLOR,
            font=self.entry_font,
            placeholder_text="Province/State",
            border_color=BORDER_COLOR,
            border_width=BORDER_WIDTH,
        )
        self.province_entry.grid(
            column=1, row=1, sticky="nsew", pady=(2.5, 0), padx=(2.5, 5)
        )

        # Radius input
        self.radius_input = ctk.CTkOptionMenu(
            master=self,
            values=["Within...", "5km", "10km", "25km", "50km"],
            text_color=TEXT_COLOR,
            dropdown_text_color=TEXT_COLOR,
            dropdown_hover_color=BUTTON_HOVER_COLOR,
            fg_color=DROP_DOWN_BG_COLOR,
            dropdown_fg_color=DROP_DOWN_BG_COLOR,
            button_color=DROP_DOWN_BG_COLOR,
            button_hover_color=DROP_DOWN_BG_COLOR,
            font=self.entry_font,
            dropdown_font=self.dropdown_font,
        )
        self.radius_input.grid(column=2, row=1, sticky="nsew")

        # Cheat score slider
        ctk.CTkSlider(
            master=self,
            from_=0,
            to=10,
            number_of_steps=100,
            fg_color=BORDER_COLOR,
            progress_color=BUTTON_HOVER_COLOR,
            button_color=BUTTON_COLOR,
            button_hover_color=BUTTON_HOVER_COLOR,
            orientation="horizontal",
            height=20,
            variable=self.cheat_score,
        ).grid(column=2, row=0, columnspan=2, sticky="ew")

        # Cheat score display
        cheat_score_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(
            master=cheat_score_frame,
            text="Cheat Level:",
            font=self.entry_font,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
        ).pack(expand=True, anchor="s")
        ctk.CTkLabel(
            master=cheat_score_frame,
            font=self.cheat_score_font,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            textvariable=self.cheat_score_display,
        ).pack(expand=True, anchor="n")
        cheat_score_frame.grid(column=4, row=0, rowspan=2, sticky="nsew", pady=3)

        # Find button
        ctk.CTkButton(
            master=self,
            text="Find!",
            font=self.button_font,
            text_color=BUTTON_TEXT_COLOR,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            command=self.button_click,
        ).grid(column=3, row=1, sticky="nsew", padx=10)

    def button_click(self):
        """Called whenever the find button is clicked"""
        if not DEV_VERSTION:
            # Store user inputs
            user_inputs = [
                self.address_entry.get(),
                self.city_entry.get(),
                self.province_entry.get(),
            ]
            radius = self.radius_input.get()
            cheat_score = round(self.cheat_score.get(), 1)

            # Verify inputs
            for string in user_inputs:
                if string == "":
                    ErrorMesage(self.parent, "Please input your locaiton information")
                    return
            if radius == "Within...":
                ErrorMesage(self.parent, "Please select a search radius.")
                return
            radius = int(radius[: radius.index("km")]) * 1000

            # Create a string for the places api
            full_address = " ".join(user_inputs)

        # Get cheat meals
        if DEV_VERSTION:
            cheat_meals = pd.read_csv("data/cheat_meals.csv").values.tolist()
            # cheat_meals = []
        else:
            # Returns a nested list of meal options
            print("radius:", radius)
            cheat_meals = get_cheat_meals(full_address, cheat_score, radius)

        # Limit the number of meals iniitially loaded since pagination is not implemented
        if len(cheat_meals) > 15:
            cheat_meals = cheat_meals[:15]

        if len(cheat_meals) > 0:
            # Store the search results as a JSON string
            self.meal_data.set(json.dumps(cheat_meals).replace("\\n", " "))
        else:
            ErrorMesage(self.parent, "No meals found!")

    def update_display(self, *args):
        """Updates the cheat score display label with the current cheat score indicated by the slidder. This is called whenever the slider is moved."""
        self.cheat_score_display.set(str(round(self.cheat_score.get(), 1)))


class MealOptionsPanel(ctk.CTkScrollableFrame):
    """This panel displays the search results as a scrollable list."""

    def __init__(
        self, parent, meal_data, data_display_num, title_label, col, row, colspan
    ):
        super().__init__(
            master=parent,
            fg_color="transparent",
            scrollbar_fg_color="transparent",
            scrollbar_button_color=DROP_DOWN_BG_COLOR,
            scrollbar_button_hover_color=BORDER_COLOR,
        )
        self.grid(
            column=col,
            row=row,
            columnspan=colspan,
            sticky="nsew",
            pady=10,
            padx=(10, 0),
        )

        # Fonts
        self.normal_font = ctk.CTkFont(family=FAMILY, size=14)

        # Data
        self.meal_data = meal_data
        # Whenever the search results srting is updated, render the search results
        self.meal_data.trace("w", self.render_meal_options)
        self.data_display_num = data_display_num
        self.title_label = title_label

        # Icon images
        img = Image.open("img/right-arrow.png")
        self.btn_img = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(64 / 256 * MEAL_OPTION_HEIGHT, MEAL_OPTION_HEIGHT),
        )
        self.establishment_img = Image.open("img/restaurant.png")
        self.location_img = Image.open("img/location-pin.png")
        self.score_img = Image.open("img/logo-icon.png")

    def render_meal_options(self, *args):
        """Called whenever the search result JSON string is updated. Displays search results as a scrollable list of cards."""
        # Clear the panel
        for child in self.winfo_children():
            child.destroy()
        # Update the header label text
        self.title_label.configure(text="Loading...")
        self.title_label.update_idletasks()

        # Load in the search results
        cheat_meals = json.loads(self.meal_data.get())
        dot = "."
        i = 3
        for j, meal in enumerate(cheat_meals):
            # Destructure the meal data
            brand, item, *nutrition, cheat_score, address, distance, __ = meal

            # Information after the "(" is typically unecessary
            try:
                item = item[: item.index("(")]
            except:
                pass

            # Cheap loading animation
            load_text = "Loading" + dot * i
            self.title_label.configure(text=load_text)
            self.title_label.update_idletasks()
            i += 1
            if i > 3:
                i = 1

            # Meal options frame
            frame = ctk.CTkFrame(
                master=self,
                fg_color=MEAL_OPTION_BG_COLOR,
                height=MEAL_OPTION_HEIGHT,
            )
            frame.pack(fill="x", padx=(0, 10))

            # Layout
            frame.columnconfigure((0, 1, 2), weight=3, uniform="a")
            frame.columnconfigure(3, weight=1, uniform="a")
            frame.rowconfigure((0, 1, 2), weight=1, uniform="a")

            # Widgets
            # Brand logo
            if brand:
                item_img_path = "logos/" + brand.replace("'", "").lower() + ".png"
                item_img = Image.open(item_img_path)
                StaticImage(
                    frame,
                    item_img,
                    MEAL_OPTION_BG_COLOR,
                    0,
                    0,
                    rowspan=3,
                    height=MEAL_OPTION_HEIGHT * 0.8,
                )

            # Restaurant name
            IconAndText(
                parent=frame,
                img=self.establishment_img,
                label_text=brand,
                col=1,
                row=0,
                colspan=2,
            )
            # Meal Item
            self.display_text = DisplayTextBox(
                parent=frame,
                text=item,
                font=self.normal_font,
                col=1,
                row=1,
                colspan=2,
                padx=(12, 0),
            )
            self.display_text.update_idletasks()

            # Distance
            IconAndText(
                parent=frame,
                img=self.location_img,
                label_text=str(round(distance, 1)) + "km",
                col=1,
                row=2,
                colspan=1,
            )
            # Cheat Score
            IconAndText(
                parent=frame,
                img=self.score_img,
                label_text=str(round(cheat_score, 1)),
                col=2,
                row=2,
                colspan=1,
            )

            # Details button
            btn = ctk.CTkButton(
                master=frame,
                text="",
                text_color=TEXT_COLOR,
                fg_color=MEAL_OPTION_BG_COLOR,
                hover_color=BORDER_COLOR,
                image=self.btn_img,
            )
            btn.grid(column=3, row=0, rowspan=3, sticky="nsew")
            btn.bind("<Button-1>", lambda event, num=j: self.button_click(event, num))

            # Spacer
            ctk.CTkFrame(master=self, fg_color="transparent", height=5).pack(fill="x")

        self.title_label.configure(text="Meal Options")

    def button_click(self, event, num):
        """Updates the data display number whenever the details button on a card is clicked. This triggers meal data window to update.

        Args:
            event (tkinter event): details button is clicked
            num (int): index of the card that was clicked
        """
        self.data_display_num.set(num)


class DataDisplayPanel(ctk.CTkFrame):
    """This panel displays all of the meal nutritional information"""

    def __init__(
        self, parent, meal_data, data_display_num, title_label, col, row, colspan
    ):
        super().__init__(
            master=parent,
            fg_color="transparent",
        )
        self.grid(
            column=col, row=row, columnspan=colspan, sticky="nsew", pady=15, padx=15
        )

        # Fonts
        self.item_font = ctk.CTkFont(family=FAMILY, size=18, weight="bold")
        self.fig_title_font = FontProperties(
            family="sans-serif", size=14, weight="bold"
        )
        self.fig_label_font = FontProperties(family="sans-serif", size=12)
        self.tiny_fig_label_font = FontProperties(family="sans-serif", size=8)
        self.button_font = ctk.CTkFont(family=FAMILY, size=18, weight="bold")

        # Data
        self.meal_data = meal_data
        self.title_label = title_label
        self.data_display_num = data_display_num
        # Update the panel
        self.data_display_num.trace("w", self.update_display)
        self.daily_values_dict = {  # https://www.canada.ca/en/health-canada/services/understanding-food-labels/percent-daily-value.html
            "Calories": [200, "cals/10"],
            "Fat": [65, "g"],
            "Saturated Fat": [20, "g"],
            "Cholesterol": [200, "mg"],
            "Sodium": [240, "mg/10"],
            "Carbs": [300, "g"],
            "Fiber": [25, "g"],
            "Sugar": [25, "g"],
            "Protein": [100, "g"],
        }

        # Layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")
        self.rowconfigure((2, 3), weight=6, uniform="a")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")

    def update_display(self, *args):
        """Updastes the data panel to display nutrition info of the currently selected meal item."""
        self.title_label.configure(text="Loading...")
        self.title_label.update_idletasks()

        # Remove the old widgets
        self.clear_data_display()

        # Get the data to display
        current_index = self.data_display_num.get()
        cheat_meals = json.loads(self.meal_data.get())

        # Destructure the data
        self.current_meal = cheat_meals[current_index]
        (
            brand,
            item,
            cals,
            total_fat,
            sat_fat,
            trans_fat,
            cholesterol,
            sodium,
            carbs,
            fiber,
            sugar,
            protein,
            cheat_score,
            address,
            distance,
            _,
        ) = self.current_meal

        # Information after the "(" is usually unecessary
        try:
            item = item[: item.index("(")]
        except:
            pass

        # Widgets
        name_button_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        name_button_frame.rowconfigure(0, weight=3, uniform="c")
        name_button_frame.rowconfigure(1, weight=1, uniform="c")
        name_button_frame.columnconfigure(0, weight=3, uniform="c")
        # Brand imgage
        item_img_path = "logos/" + brand.replace("'", "").lower() + ".png"
        item_img = Image.open(item_img_path)
        StaticImage(
            parent=name_button_frame,
            image=item_img,
            color=BG_COLOR,
            row=0,
            col=0,
        )
        ctk.CTkButton(
            master=name_button_frame,
            text="Directions",
            font=self.button_font,
            text_color=BUTTON_TEXT_COLOR,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            command=lambda: self.button_click(address),
        ).grid(
            column=0,
            row=1,
        )
        name_button_frame.grid(
            row=1,
            column=0,
        )

        # Item name
        item_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        item_frame.rowconfigure(0, weight=1, uniform="f")
        item_frame.rowconfigure(1, weight=5, uniform="f")
        item_frame.columnconfigure(0, weight=1, uniform="f")
        DisplayTextBox(
            parent=item_frame,
            text=item,
            font=self.item_font,
            col=0,
            row=1,
            colspan=1,
        )
        item_frame.grid(column=1, row=1, sticky="nsew")

        # Macros table
        self.create_macro_panel(
            cals, protein, carbs, total_fat, sugar, sodium, fiber, cholesterol
        )

        # Macros Pie Chart
        macros = [total_fat * 9 / cals, protein * 4 / cals, carbs * 4 / cals]
        pie_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        pie_frame.grid(
            column=0,
            row=2,
            sticky="nsew",
            pady=(DATA_PADY_TOP, 0),
            padx=DATA_PADX,
        )
        self.create_pie_chart_panel(
            parent=pie_frame,
            labels=["Fat", "Protein", "Carbs"],
            values=macros,
            colors=[ORANGE, RED, GREEN],
        )

        # Caloric Density Bar Graph
        cal_density_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        cal_density_frame.grid(
            column=1,
            row=2,
            columnspan=2,
            sticky="nsew",
            pady=(DATA_PADY_TOP, 0),
            padx=DATA_PADX,
        )
        caloric_density = cals / (
            total_fat + protein + carbs
        )  # Not correct but fine for this application
        self.create_bar_chart_panel(
            parent=cal_density_frame,
            densities=[caloric_density, 4.8, 1.7, 0.6],
            items=[item, "Frozen Pizza", "Potatoe", "Broccoli"],
        )

        # DV Comparasion Bar Graph
        dv_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        dv_frame.grid(
            column=0,
            row=3,
            columnspan=3,
            sticky="nsew",
            pady=(0, DATA_PADY_TOP),
        )
        actual_values = [
            cals / 10,
            total_fat,
            sat_fat,
            cholesterol,
            sodium / 10,
            carbs,
            fiber,
            sugar,
            protein,
        ]
        labels = [
            "Calories",
            "Fat",
            "Saturated Fat",
            "Cholesterol",
            "Sodium",
            "Carbs",
            "Fiber",
            "Sugar",
            "Protein",
        ]
        self.create_double_bar_chart_panel(
            parent=dv_frame,
            daily_values_dict=self.daily_values_dict,
            actual_values=actual_values,
            labels=labels,
        )

        # Return header to normal state
        self.title_label.configure(text="Meal Data")
        self.title_label.update_idletasks()

    def button_click(self, address):
        base_url = "https://www.google.com/maps/dir/?api=1"
        destination = address.replace(" ", "+")
        url = f"{base_url}&destination={destination}"
        webbrowser.open(url)

    def create_macro_panel(
        self, cals, protein, carbs, total_fat, sugar, sodium, fiber, cholesterol
    ):
        """Creates a panel which displays the name and amount of all of the majour macro and micro nutruients from the data set

        Args:
            cals (double): meal calories
            protein (double): protein content
            carbs (double): carbohydrate content
            total_fat (intdouble): fat content
            sugar (double): sugar content
            sodium (double): sodium content
            fiber (double): fiber content
            cholesterol (double): cholesterol content
        """
        macro_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        # Layout
        macro_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform="b")
        macro_frame.columnconfigure(0, weight=9, uniform="b")
        macro_frame.columnconfigure(1, weight=12, uniform="b")

        # Calories
        MacroWidget(
            parent=macro_frame,
            macro_name="Calories: ",
            value=cals,
            units="",
            col=0,
            row=0,
        )
        # Protein
        MacroWidget(
            parent=macro_frame,
            macro_name="Protein: ",
            value=protein,
            units="g",
            col=0,
            row=1,
        )
        MacroWidget(
            parent=macro_frame,
            macro_name="Carbs: ",
            value=carbs,
            units="g",
            col=0,
            row=2,
        )
        # Fat
        MacroWidget(
            parent=macro_frame,
            macro_name="Fat: ",
            value=total_fat,
            units="g",
            col=0,
            row=3,
        )
        # Sugar
        MacroWidget(
            parent=macro_frame,
            macro_name="Sugar ",
            value=sugar,
            units="g",
            col=1,
            row=0,
        )
        # Sodium
        MacroWidget(
            parent=macro_frame,
            macro_name="Sodium: ",
            value=sodium,
            units="mg",
            col=1,
            row=1,
        )
        # Fiber
        MacroWidget(
            parent=macro_frame,
            macro_name="Fiber: ",
            value=fiber,
            units="g",
            col=1,
            row=2,
        )
        # Cholesterol
        MacroWidget(
            parent=macro_frame,
            macro_name="Cholesterol: ",
            value=cholesterol,
            units="mg",
            col=1,
            row=3,
        )
        macro_frame.grid(column=2, row=1, sticky="nsew")

    def create_pie_chart_panel(self, parent, labels, values, colors):
        """Creates a pie chart to display the values and associated labels

        Args:
            parent (CTkFrame):
            labels ([str]): slice labels
            values ([double]): percetage sizes of each slice
            colors ([str]): hexadecimal strings which are the slice colors
        """
        # Create a Figure object and add a subplot
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        # Create the pie chart and add it to the subplot
        ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%")
        ax.axis("equal")

        # Create the title
        ax.set_title("Calorie Contributions", fontproperties=self.fig_title_font)

        # Set font properties for labels
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(self.fig_label_font)

        # Create a canvas and add the figure to it
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()

        # Add the canvas to the CustomTkinter window using grid layout
        canvas.get_tk_widget().pack()

    def create_bar_chart_panel(self, parent, densities, items):
        """Creats a bar chart to compare caloric density values

        Args:
            parent (CTkFrame):
            densities ([double]): caloric densities to be displayed
            items ([str]): food items associated with the caloric densities
        """
        # Create a figure object
        fig = Figure(figsize=(4, 3), dpi=100)
        fig.subplots_adjust(bottom=0.2)

        # Add a subplot
        ax = fig.add_subplot(111)

        # Wrap label text
        for i, item in enumerate(items):
            items[i] = "\n".join(textwrap.wrap(item, 12))

        # Data for the bar chart
        x = items
        x_ticks = range(len(x))
        y = densities

        # Create the bar chart
        ax.bar(x, y, color=YELLOW)

        # Set the title and axis labels
        ax.set_title("Caloric Densities", fontproperties=self.fig_title_font)
        ax.set_ylabel("Calories/g")

        # Set font properties for labels
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(self.tiny_fig_label_font)

        # Remove graph border
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Create a canvas to display the figure
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()

        canvas.get_tk_widget().pack()

    def create_double_bar_chart_panel(
        self, parent, daily_values_dict, actual_values, labels
    ):
        """Creates a double bar chart which is used to compare the nutrient content of the meal item with the recommended daily values for the nutrient

        Args:
            parent (CTkFrame):
            daily_values_dict (object): dictionary where the keys are the x-axis labels and the values are a list containing the values and units
            actual_values ([double]): meal item nutrient values
            labels ([str]): x-axis labels
        """
        axis_labels = []
        daily_values = []
        for label in labels:
            axis_labels.append(
                label.replace(" ", "\n") + "\n" + daily_values_dict[label][1]
            )
            daily_values.append(daily_values_dict[label][0])

        # Create a Figure object and add a subplot
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.subplots_adjust(bottom=0.2)

        # Bar width
        width = 0.35

        # Create the double bar graph
        ax.bar(
            range(len(axis_labels)),
            daily_values,
            width,
            color=GREEN,
            label="Recommended DV",
        )
        ax.bar(
            [i + width for i in range(len(axis_labels))],
            actual_values,
            width,
            color=YELLOW,
            label="Actual",
        )

        # Set the x-axis tick positions and labels
        ax.set_xticks([i + width / 2 for i in range(len(axis_labels))])
        ax.set_xticklabels(axis_labels)

        # Remove graph border
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Set the title and axis label
        ax.set_title("Daily Values", fontproperties=self.fig_title_font)
        ax.set_ylabel("Amount")

        # Set font properties for labels
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(self.tiny_fig_label_font)

        # Add a legend
        ax.legend()

        # Create a canvas and add the figure to it
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()

        # Add the canvas to the Tkinter window
        canvas.get_tk_widget().pack()

    def clear_data_display(self):
        """Clear the widgets contained in a grid cell"""
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()
