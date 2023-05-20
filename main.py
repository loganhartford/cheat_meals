#! .\.venv\scripts\python.exe
from settings import *
import customtkinter as ctk
from versions import MobileVersion, DesktopVersion
from PIL import Image

# For setting the title bar color on widnows
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.title_bar_color(BG_COLOR)
        self.geometry("1400x900")
        self.minsize(375, 667)  # iPhone SE height
        self.title("")
        self.iconbitmap("icons/logo.ico")

        # Data
        self.logo_png = Image.open("img/logo.png")
        self.cheat_score = ctk.DoubleVar()
        self.cheat_score.set(5.0)
        self.meal_data = ctk.StringVar()  # Stores the search results as a JSON string
        self.data_display_num = (
            ctk.IntVar()
        )  # Controls which search result is being displayed
        self.data_display_num.set(-1)

        # Starting version
        self.version = DesktopVersion(
            self, self.logo_png, self.cheat_score, self.meal_data, self.data_display_num
        )

        # States
        self.width_break = 700
        self.mobile_version_bool = ctk.BooleanVar(value=False)
        # Uncomment next line to allow switching to mobile version
        # self.bind("<Configure>", self.check_size)
        self.mobile_version_bool.trace("w", self.change_size)

        self.protocol(
            "WM_DELETE_WINDOW", self.quit
        )  # This stops the program from crashing when the window closes (matplotlib)
        self.mainloop()

    def check_size(self, event):
        """Determines if the current window size is above or below any of the breakpoints and set's the state variable accordingly

        Args:
            event (tkinter.event): event occurs whenever the window is moved or resized
        """
        if event.widget != self:  # Only care if the window is being resized
            return
        if self.mobile_version_bool.get():
            if event.width > self.width_break:
                self.mobile_version_bool.set(False)
        else:
            if event.width < self.width_break:
                self.mobile_version_bool.set(True)

    def change_size(self, *args):
        """When the state vairables change, this funciton is called to update the display to match the state described by the state varables"""
        self.version.pack_forget()
        # Mobile verion
        if self.mobile_version_bool.get():
            self.version = MobileVersion(
                self, self.logo_png, self.cheat_score, self.meal_data
            )
        else:
            self.version = DesktopVersion(
                self,
                self.logo_png,
                self.cheat_score,
                self.meal_data,
                self.data_display_num,
            )

    def title_bar_color(self, color):
        """This changes the window title bar color to the specified color when the program is run on a windos computer.

        Args:
            color (str): Hexadecimal string eg."#282828"
        """
        try:
            HNWD = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            windll.dwmapi.DwmSetWindowAttribute(
                HNWD, DWMWA_ATTRIBUTE, byref(c_int(color)), sizeof(c_int)
            )
        except:
            pass


if __name__ == "__main__":
    App()
