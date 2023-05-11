#! .\.venv\scripts\python.exe
from settings import *
import customtkinter as ctk
from versions import MobileVersion, DesktopVersion

# For setting the title bar color on widnows
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.title_bar_color(BG_COLOR)
        self.geometry("1000x844")
        self.minsize(375, 667)  # iPhone SE
        self.maxsize(0, 844)  # iPhone 12 Pro height
        self.title("")
        self.iconbitmap("icons/empty.ico")

        # Initial version
        self.version = DesktopVersion(self)

        # States
        self.width_break = 700
        self.mobile_version_bool = ctk.BooleanVar(value=False)
        self.bind("<Configure>", self.check_size)
        self.mobile_version_bool.trace("w", self.change_size)

        self.mainloop()

    def check_size(self, event):
        if event.widget != self:
            return
        if self.mobile_version_bool.get():
            if event.width > self.width_break:
                self.mobile_version_bool.set(False)
        else:
            if event.width < self.width_break:
                self.mobile_version_bool.set(True)
        print(event.height, event.width, self.mobile_version_bool.get())

    def change_size(self, *args):
        self.version.pack_forget()
        # Mobile verion
        if self.mobile_version_bool.get():
            self.version = MobileVersion(self)
        else:
            self.version = DesktopVersion(self)

    def title_bar_color(self, color):
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
