from tkinter import Canvas
from PIL import ImageTk


class StaticImage(Canvas):
    """Creates a canvas and places and image on it and attached methods to resizing events to keeps the image properly sized."""

    def __init__(
        self, parent, image, color, row, col, rowspan=1, height=None, width=None
    ):
        super().__init__(
            master=parent,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            background=color,
            height=height,
            width=width,
        )
        self.grid(column=col, row=row, rowspan=rowspan, sticky="nsew")

        # Image data
        self.image = image
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]

        # Start values
        self.canvas_width = 0
        self.canvas_height = 0
        self.image_width = 0
        self.image_height = 0

        # Event
        self.bind("<Configure>", self.resize)

    def resize(self, event=None):
        """Called whenever the image is resized. Looks at the aspect ratio of the canvas and sized the image to correctly fit the canvas."""
        canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height

        # Resize image
        if canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.update_image()

    def update_image(self):
        """Deletes the current image and replaces with the a resized image."""
        self.delete("all")
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )
