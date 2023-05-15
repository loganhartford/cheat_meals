from customtkinter import CTkFrame
from panels import *


class MobileVersion(CTkFrame):
    def __init__(self, parent, logo_img, cheat_score, meal_data):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill="both")

        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=5, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")

        # Widgets
        LogoPanel(self, logo_img, 0, 0)


class DesktopVersion(CTkFrame):
    def __init__(self, parent, logo_img, cheat_score, meal_data, data_display_num):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill="both")

        # Fonts
        self.title_font = ctk.CTkFont(family=FAMILY, size=28, weight="bold")

        # Layout
        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.rowconfigure(2, weight=16, uniform="a")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.columnconfigure(3, weight=6, uniform="a")

        # Widgets
        LogoPanel(self, logo_img, 0, 0)
        UserInputPanel(self, cheat_score, meal_data, 1, 0, 3)
        # Meal Options Header
        self.meal_options_header_label = self.create_header("Meal Options", 0, 1, 3)
        MealOptionsPanel(
            self, meal_data, data_display_num, self.meal_options_header_label, 0, 2, 3
        )
        # Data Display Header
        self.meal_data_header_label = self.create_header("Meal Data", 3, 1, 3)
        DataDisplayPanel(
            self, meal_data, data_display_num, self.meal_data_header_label, 3, 2, 1
        )

    def create_header(self, heading, col, row, colspan):
        # Meal Options Header
        options_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_header_frame.grid(
            column=col, row=row, columnspan=colspan, sticky="nsew"
        )
        title_label = ctk.CTkLabel(
            master=options_header_frame,
            text=heading,
            height=30,
            fg_color="transparent",
            font=self.title_font,
            text_color=BUTTON_COLOR,
        )
        title_label.pack(fill="x", padx=(0, 10))
        ctk.CTkFrame(
            master=options_header_frame, fg_color=MEAL_OPTION_HEADER, height=5
        ).pack(fill="x", pady=(0, 10), padx=(0, 10))

        return title_label
