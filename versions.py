from customtkinter import CTkFrame
from panels import *


class MobileVersion(CTkFrame):
    """This class is used to display the mobile version of the application.
    It is currently useless as I have not have time to build it out.

    Args:
        CTkFrame (_type_): _description_
    """

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
    """This class is used to display the desktop (default) version of the application."""

    def __init__(self, parent, logo_img, cheat_score, meal_data, data_display_num):
        """init

        Args:
            parent (tkinter window or frame):
            logo_img (PIL Image): Application logo
            cheat_score (DoubleVar): Current cheat score set my the slider
            meal_data (StringVar): Search results stored as a JSON string
            data_display_num (int): Controls which search result is being displayed in the data panel
        """
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
        """Creates a header section composed of a labels and a frames used to underline the label

        Args:
            heading (str): heading text
            col (int):
            row (int):
            colspan (int):

        Returns:
            CTkLabel: returns the label so it can stored and updated in other parts of the application
        """
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
