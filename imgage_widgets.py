from tkinter import Canvas
from PIL import ImageTk


class StaticImage(Canvas):
    def __init__(self, parent, image, row, col):
        super().__init__(
            master=parent,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            background="white",
        )
        self.grid(column=col, row=row, sticky="nsew")

        # Image ratio
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
        print(event.height, event.width)
        canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height

        # Resize
        if canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.update_image()

    def update_image(self):
        self.delete("all")
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )
