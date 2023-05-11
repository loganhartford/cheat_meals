from customtkinter import CTkFrame


class MobileVersion(CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill="both")

        self.rowconfigure(0, weigh=1, uniform="a")
        self.rowconfigure(1, weigh=5, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")


class DesktopVersion(CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill="both")

        self.rowconfigure(0, weigh=1, uniform="a")
        self.rowconfigure(1, weigh=5, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")
