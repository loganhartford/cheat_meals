import customtkinter as ctk
from settings import *
from imgage_widgets import StaticImage
from PIL import Image


class IconAndText(ctk.CTkFrame):
    def __init__(self, parent, img, label_text, col, row, colspan):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col,
            row=row,
            columnspan=colspan,
            sticky="s",
            padx=(5, 0),
            pady=(5, 0),
        )

        # Fonts
        self.normal_font = ctk.CTkFont(family=FAMILY, size=14)

        # Data
        self.ctk_img = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(14, 14),
        )

        # Layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2 * colspan, uniform="a")

        # Img button
        btn = ctk.CTkButton(
            master=self,
            text="",
            text_color=TEXT_COLOR,
            fg_color="transparent",
            hover=False,
            image=self.ctk_img,
        )
        btn.grid(column=0, row=0, rowspan=3, sticky="nsew")
        btn.configure(cursor="arrow")

        ctk.CTkLabel(
            master=self,
            font=self.normal_font,
            fg_color="transparent",
            text_color=TEXT_COLOR,
            text=label_text,
            anchor="w",
        ).grid(column=1, row=0, sticky="nsew", padx=(5, 0))
