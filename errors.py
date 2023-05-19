from CTkMessagebox import CTkMessagebox
from settings import *


class ErrorMesage(CTkMessagebox):
    """Displays an pop up window with and error message

    Pass in a string containing an error message.
    """

    def __init__(self, parent, error_text):
        super().__init__(
            master=parent,
            title="",
            fg_color=BG_COLOR,
            bg_color=BG_COLOR,
            message=error_text,
            text_color=TEXT_COLOR,
            button_text_color=BUTTON_TEXT_COLOR,
            button_color=BUTTON_COLOR,
            button_hover_color=BUTTON_HOVER_COLOR,
            cancel_button_color="transparent",
            icon="cancel",
            corner_radius=8,
            font=(FAMILY, 14),
            border_color=BORDER_COLOR,
        )
