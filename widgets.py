import customtkinter as ctk
from settings import *
from imgage_widgets import StaticImage
from PIL import Image


class IconAndText(ctk.CTkFrame):
    def __init__(self, parent, icon_path, text, col, row, colspan):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col,
            row=row,
            columnspan=colspan,
            sticky="w",
            padx=(5, 0),
            pady=(5, 0),
        )

        # Fonts
        self.normal_font = ctk.CTkFont(family=FAMILY, size=14)

        # Data
        brand_img = Image.open(icon_path)

        # Layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=8, uniform="a")

        StaticImage(self, brand_img, MEAL_OPTION_BG_COLOR, 0, 0, height=20, width=20)
        ctk.CTkLabel(
            master=self,
            font=self.normal_font,
            fg_color="transparent",
            text_color=TEXT_COLOR,
            text=text,
        ).grid(column=1, row=0, sticky="w", padx=(5, 0))
