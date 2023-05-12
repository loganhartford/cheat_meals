from customtkinter import CTkFrame
from panels import *


class MobileVersion(CTkFrame):
    def __init__(self, parent, logo_img, cheat_score):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill="both")

        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=5, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")

        # Widgets
        LogoPanel(self, logo_img, 0, 0)


class DesktopVersion(CTkFrame):
    def __init__(self, parent, logo_img, cheat_score):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill="both")

        # Layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=8, uniform="a")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.columnconfigure(3, weight=6, uniform="a")

        # Widgets
        LogoPanel(self, logo_img, 0, 0)
        UserInputPanel(self, cheat_score, 1, 0, 3)
        MealOptionsPanel(self, 0, 1, 3)

        # ctk.CTkFrame(master=self, fg_color="blue").grid(column=1, row=0, sticky="nsew")
        # ctk.CTkFrame(master=self, fg_color="green").grid(column=0, row=1, sticky="nsew")
        # ctk.CTkFrame(master=self, fg_color="yellow").grid(
        #     column=1, row=1, sticky="nsew"
        # )
