import customtkinter as ctk
from settings import *
from imgage_widgets import StaticImage
from PIL import Image


class IconAndText(ctk.CTkFrame):
    """Used to create a frame which contains and icon and a small piece of text side by side."""

    def __init__(self, parent, img, label_text, col, row, colspan):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(
            column=col,
            row=row,
            columnspan=colspan,
            sticky="s",
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

        # Img button (just houses the icon)
        btn = ctk.CTkButton(
            master=self,
            text="",
            text_color=TEXT_COLOR,
            fg_color="transparent",
            hover=False,
            image=self.ctk_img,
        )
        btn.grid(column=0, row=0, rowspan=3, sticky="nsew")
        # Prevent hand cursor on hover
        btn.configure(cursor="arrow")

        ctk.CTkLabel(
            master=self,
            font=self.normal_font,
            fg_color="transparent",
            text_color=TEXT_COLOR,
            text=label_text,
            anchor="w",
        ).grid(column=1, row=0, sticky="nsew")


class DisplayTextBox(ctk.CTkTextbox):
    """Creates a scrollable text box to disolay the food item. The food items are usually long and this box wraps the text and makes it scrollable.

    Args:
        ctk (_type_): _description_
    """

    def __init__(self, parent, text, font, col, row, colspan, padx=None):
        super().__init__(
            master=parent,
            font=font,
            fg_color="transparent",
            border_width=0,
            activate_scrollbars=False,
            text_color=TEXT_COLOR,
            wrap="word",
            height=0,
        )
        self.grid(column=col, row=row, columnspan=colspan, sticky="nsew", padx=padx)

        # Display the text
        self.insert("0.0", f"{text}")
        # Disable the entry feature of the box
        self.configure(state="disabled")
        # Prevent the text entry cursor on hover
        self.configure(cursor="arrow")


class MacroWidget(ctk.CTkFrame):
    """Creates a frame which houses two labels. One is bolded and contains the name of the nutrient, the other is normal weight and contains the value."""

    def __init__(self, parent, macro_name, value, units, col, row):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(column=col, row=row, sticky="nsew")

        # Fonts
        self.macro_font = ctk.CTkFont(family=FAMILY, size=14, weight="bold")
        self.value_font = ctk.CTkFont(family=FAMILY, size=14)

        # Nutrient name
        ctk.CTkLabel(
            master=self,
            text=macro_name,
            fg_color="transparent",
            text_color=TEXT_COLOR,
            font=self.macro_font,
            anchor="w",
        ).pack(side="left")

        # Nutrient label
        ctk.CTkLabel(
            master=self,
            text=str(int(round(value, 0))) + units,
            fg_color="transparent",
            text_color=TEXT_COLOR,
            font=self.value_font,
            anchor="w",
        ).pack(side="left")
