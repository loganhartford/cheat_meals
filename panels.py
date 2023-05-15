import customtkinter as ctk
from imgage_widgets import StaticImage
from settings import *
from data import get_cheat_meals
from errors import ErrorMesage
import json
from PIL import Image, ImageTk
from widgets import IconAndText, DisplayTextBox, MacroWidget
from get_images import download_image
from os import remove
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
import textwrap

# delete later (return a list)
import pandas as pd


class LogoPanel(ctk.CTkFrame):
    def __init__(self, parent, logo_img, col, row):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(column=col, row=row, sticky="nsew", pady=10, padx=10)

        # Layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        # Widgets
        StaticImage(self, logo_img, "white", 0, 0)


class UserInputPanel(ctk.CTkFrame):
    def __init__(self, parent, cheat_score, meal_data, col, row, colspan):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col, row=row, columnspan=colspan, sticky="nsew", pady=10, padx=10
        )

        # Fonts
        self.entry_font = ctk.CTkFont(family=FAMILY, size=20)
        self.dropdown_font = ctk.CTkFont(family=FAMILY, size=14)
        self.cheat_score_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")
        self.button_font = ctk.CTkFont(family=FAMILY, size=20, weight="bold")

        # Data
        self.cheat_score = cheat_score
        self.cheat_score_display = ctk.StringVar()
        self.update_display()
        self.cheat_score.trace("w", self.update_display)
        self.meal_data = meal_data

        # Layout
        self.columnconfigure(
            (
                0,
                1,
            ),
            weight=3,
            uniform="a",
        )
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

        # Cheat score input
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

    def button_click(self):
        # Store user inputs
        user_inputs = [
            self.address_entry.get(),
            self.city_entry.get(),
            self.province_entry.get(),
        ]
        radius = self.radius_input.get()
        cheat_score = round(self.cheat_score.get(), 1)

        # # Verify inputs
        # for string in user_inputs:
        #     if string == "":
        #         ErrorMesage(self, "Please input your locaiton information")
        #         return
        # if radius == "Within...":
        #     ErrorMesage(self, "Please select a search radius.")
        #     return

        full_address = " ".join(user_inputs)

        # Get cheat meals
        # cheat_meals = get_cheat_meals(full_address, cheat_score, radius)
        cheat_meals = pd.read_csv("cheat_meals.csv").values.tolist()
        self.meal_data.set(json.dumps(cheat_meals).replace("\\n", " "))

    def update_display(self, *args):
        self.cheat_score_display.set(str(round(self.cheat_score.get(), 1)))


class MealOptionsPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, meal_data, data_display_num, col, row, colspan):
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
        self.title_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")
        self.normal_font = ctk.CTkFont(family=FAMILY, size=14)

        # Data
        self.meal_data = meal_data
        self.meal_data.trace("w", self.render_meal_options)
        self.data_display_num = data_display_num

        # Images
        img = Image.open("img/right-arrow.png")
        self.btn_img = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(64 / 256 * MEAL_OPTION_HEIGHT, MEAL_OPTION_HEIGHT),
        )
        self.establishment_img = Image.open("img/restaurant.png")
        self.location_img = Image.open("img/location-pin.png")
        self.score_img = Image.open("img/score.png")

        self.title_label = ctk.CTkLabel(
            self,
            text="Meal Options",
            height=30,
            fg_color="transparent",
            font=self.title_font,
            text_color=BUTTON_COLOR,
        )
        self.title_label.pack(fill="x", padx=(0, 10))
        ctk.CTkFrame(master=self, fg_color=MEAL_OPTION_HEADER, height=5).pack(
            fill="x", pady=(0, 10), padx=(0, 10)
        )

    def render_meal_options(self, *args):
        self.title_label.configure(text="Loading...")
        self.title_label.update_idletasks()

        cheat_meals = json.loads(self.meal_data.get())
        dot = "."
        i = 3
        for j, meal in enumerate(cheat_meals):
            brand, item, *nutrition, cheat_score, address, distance, __ = meal

            try:
                item = item[: item.index("(")]  # improves search results
            except:
                pass

            # Cheap loading animation
            load_text = "Loading" + dot * i
            self.title_label.configure(text=load_text)
            self.title_label.update_idletasks()
            i += 1
            if i > 3:
                i = 1

            # Meal options
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

            query = brand + " " + item
            # item_img_path = download_image(query, "temp", "temp_img")
            item_img_path = "logos/" + brand.lower() + ".png"
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
            # remove(item_img_path)

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
            DisplayTextBox(
                parent=frame,
                text=item,
                font=self.normal_font,
                col=1,
                row=1,
                colspan=2,
                padx=(12, 0),
            )

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

    def create_laoding_frame(self):
        self.loading_frame = ctk.CTkFrame(master=self, fg_color=MEAL_OPTION_BG_COLOR)
        self.loading_frame.pack(expand=True, fill="both")
        ctk.CTkLabel(master=self.loading_frame, text="loading...").pack(
            expand=True, fill="both"
        )
        return

    def button_click(self, event, num):
        self.data_display_num.set(num)


class DataDisplayPanel(ctk.CTkFrame):
    def __init__(self, parent, meal_data, data_display_num, col, row, colspan):
        super().__init__(
            master=parent,
            fg_color="transparent",
        )
        self.grid(
            column=col, row=row, columnspan=colspan, sticky="nsew", pady=15, padx=15
        )

        # Fonts
        self.item_font = ctk.CTkFont(family=FAMILY, size=18, weight="bold")
        self.title_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")
        self.fig_title_font = FontProperties(
            family="sans-serif", size=14, weight="bold"
        )
        self.fig_label_font = FontProperties(family="sans-serif", size=12)
        self.tiny_fig_label_font = FontProperties(family="sans-serif", size=8)

        # Data
        self.meal_data = meal_data
        self.data_display_num = data_display_num
        self.data_display_num.trace("w", self.update_display)

        # Layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")
        self.rowconfigure((2, 3), weight=6, uniform="a")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")

        title_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        title_frame.grid(column=0, row=0, columnspan=3, sticky="nsew")
        self.title_label = ctk.CTkLabel(
            master=title_frame,
            text="Meal Data",
            height=30,
            fg_color="transparent",
            font=self.title_font,
            text_color=BUTTON_COLOR,
        )
        self.title_label.pack(fill="x", padx=(0, 10))
        ctk.CTkFrame(master=title_frame, fg_color=MEAL_OPTION_HEADER, height=5).pack(
            fill="x", pady=(0, 10), padx=(0, 10)
        )

    def update_display(self, *args):
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
        try:
            item = item[: item.index("(")]  # improves search results
        except:
            pass

        # Widgets
        # Item imgage
        query = brand + " " + item
        item_img_path = download_image(query, "temp", "temp_img")
        item_img = Image.open(item_img_path)
        StaticImage(
            parent=self,
            image=item_img,
            color=BG_COLOR,
            row=1,
            col=0,
        )
        remove(item_img_path)

        # Item name
        # ctk.CTkLabel(
        #     master=self,
        #     text=item,
        #     fg_color="red",
        #     text_color=TEXT_COLOR,
        #     font=self.item_font,
        #     anchor="w",
        # ).grid(column=1, row=1, sticky="nsew")
        DisplayTextBox(
            parent=self,
            text=item,
            font=self.item_font,
            col=1,
            row=1,
            colspan=1,
        )

        # Macros
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
            pady=(DATA_PADY_TOP, DATA_PADY),
            padx=DATA_PADX,
        )
        self.create_pie_chart_panel(
            parent=pie_frame,
            labels=["Fat", "Protein", "Carbs"],
            values=macros,
            colors=["#f4a261", "#e76f51", "#2a9d8f"],
        )

        # Caloric Density Bar Graph
        cal_density_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        cal_density_frame.grid(
            column=1,
            row=2,
            columnspan=2,
            sticky="nsew",
            pady=(DATA_PADY_TOP, DATA_PADY),
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

        # Return header to normal state
        self.title_label.configure(text="Meal Data")
        self.title_label.update_idletasks()

    def create_macro_panel(
        self, cals, protein, carbs, total_fat, sugar, sodium, fiber, cholesterol
    ):
        macro_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        # Layout
        macro_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform="b")
        macro_frame.columnconfigure(0, weight=9, uniform="b")
        macro_frame.columnconfigure(1, weight=12, uniform="b")

        MacroWidget(
            parent=macro_frame,
            macro_name="Calories: ",
            value=cals,
            units="",
            col=0,
            row=0,
        )
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
        MacroWidget(
            parent=macro_frame,
            macro_name="Fat: ",
            value=total_fat,
            units="g",
            col=0,
            row=3,
        )
        MacroWidget(
            parent=macro_frame,
            macro_name="Sugar ",
            value=sugar,
            units="g",
            col=1,
            row=0,
        )
        MacroWidget(
            parent=macro_frame,
            macro_name="Sodium: ",
            value=sodium,
            units="mg",
            col=1,
            row=1,
        )
        MacroWidget(
            parent=macro_frame,
            macro_name="Fiber: ",
            value=fiber,
            units="g",
            col=1,
            row=2,
        )
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
        # Create a Figure object and add a subplot
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        # Create the pie chart and add it to the subplot
        ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%")
        ax.axis("equal")
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
        # Create a figure object
        fig = Figure(figsize=(4, 3), dpi=100)
        fig.subplots_adjust(bottom=0.4)

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
        ax.bar(x, y, color="#e9c46a")

        # Set the title and axis labels
        ax.set_title("Caloric Densities", fontproperties=self.fig_title_font)
        ax.set_xlabel("Food Item")
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

    def clear_data_display(self):
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()


""" 
To Do:
- Display the DV graph
- Need to clear previous search when find button is clicked again
- turn safe search on for the google search api
- Disable the mobile version
"""
