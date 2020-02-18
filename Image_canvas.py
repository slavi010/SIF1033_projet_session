import cv2
import numpy as np
from PIL import Image, ImageTk
import Tkinter as tk
import matplotlib.pyplot as plt


class Image_canvas:
    def __init__(self, canvas):
        # RGB
        self.image_canvas = None
        self.image_cv2 = None
        self.start_image_cv2 = None

        self.canvas = canvas

    def set_image(self, image_cv2_bgr):
        self.start_image_cv2 = cv2.cvtColor(image_cv2_bgr, cv2.COLOR_BGR2RGB)
        self.image_cv2 = self.start_image_cv2

    def update_image_canvas(self, image_arg):
        if self.image_canvas is not None:
            self.canvas.delete(self.image_canvas)
        self.image_canvas = self.canvas.create_image(0, 0, image=image_arg, anchor=tk.NW)

    # resize image_cv2
    def resize(self, new_height, new_width=None):
        height, width, no_channels = self.start_image_cv2.shape

        if new_width is None:
            new_width = (new_height/height) * width

        self.image_cv2 = cv2.resize(self.start_image_cv2, (new_width, new_height))
        self.start_image_cv2 = self.image_cv2