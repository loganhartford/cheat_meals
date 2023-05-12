import customtkinter as ctk
from imgage_widgets import StaticImage
from settings import *
from data import get_cheat_meals
from CTkMessagebox import CTkMessagebox
from errors import ErrorMesage


class LogoPanel(ctk.CTkFrame):
    def __init__(self, parent, logo_img, col, row):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(column=col, row=row, sticky="nsew", pady=10, padx=10)

        # Layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        # Widgets
        StaticImage(self, logo_img, 0, 0)


class UserInputPanel(ctk.CTkFrame):
    def __init__(self, parent, cheat_score, col, row, colspan):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col, row=row, columnspan=colspan, sticky="nsew", pady=10, padx=10
        )

        # Data
        self.entry_font = ctk.CTkFont(family=FAMILY, size=20)
        self.dropdown_font = ctk.CTkFont(family=FAMILY, size=14)
        self.cheat_score_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")
        self.button_font = ctk.CTkFont(family=FAMILY, size=20, weight="bold")
        self.cheat_score = cheat_score
        self.cheat_score_display = ctk.StringVar()
        self.update_display()
        self.cheat_score.trace("w", self.update_display)

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

        # Verify inputs
        for string in user_inputs:
            if string == "":
                ErrorMesage(self, "Please input your locaiton information")
                return
        if radius == "Within...":
            ErrorMesage(self, "Please select a search radius.")
            return

        full_address = " ".join(user_inputs)
        # cheat_meals_df = get_cheat_meals(full_address, cheat_score, radius)

    # def render_error(self, error_text):
    #     top = ctk.CTkToplevel(fg_color=BG_COLOR)
    #     top.geometry("")

    def update_display(self, *args):
        self.cheat_score_display.set(str(round(self.cheat_score.get(), 1)))


class MealOptionsPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, col, row, colspan):
        super().__init__(
            master=parent,
            fg_color="transparent",
            scrollbar_fg_color="transparent",
            scrollbar_button_color=DROP_DOWN_BG_COLOR,
            scrollbar_button_hover_color=BORDER_COLOR,
        )
        self.grid(
            column=col, row=row, columnspan=colspan, sticky="nsew", pady=10, padx=10
        )

        # Data
        self.title_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")

        ctk.CTkLabel(
            self,
            text="Meal Options",
            height=MEAL_OPTION_HEIGHT / 1.5,
            fg_color=BORDER_COLOR,
            font=self.title_font,
            text_color=TEXT_COLOR,
        ).pack(fill="x")
