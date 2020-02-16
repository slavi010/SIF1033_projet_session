# coding=utf-8


import Tkinter as tk

from File import File
import cv2 as cv2
from PIL import Image, ImageTk

from Image_Builder import Image_Builder
from Image_canvas import Image_canvas

from time import sleep

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


# root.mainloop()
from Menu import Menu


class Fenetre:

    def __init__(self):
        # fenetre de l'image
        self.root = tk.Tk()

        # canvas de l'image
        self.canvas_image_WIDTH = 1280
        self.canvas_image_HEIGHT = 720

        self.canvas_image = tk.Canvas(
            self.root,
            width=self.canvas_image_WIDTH,
            height=self.canvas_image_HEIGHT)
        self.canvas_image.grid(row=0, column=0)

        self.image = Image_canvas(self.canvas_image)

        # menu && slider
        self.menu = Menu(self)

    def show_image(self, image_path=None, camera=False):
        cap = None

        if camera:
            cap = cv2.VideoCapture(0)

        while True:
            if cap is not None:
                ret, frame = cap.read()
                self.image.set_image(frame)
            else:
                if image_path is None:
                    image_path = File.get_image(self.root)
                self.image.set_image(cv2.imread(image_path))

            self.image.resize(self.canvas_image_WIDTH, self.canvas_image_HEIGHT)

            if self.menu.outils_contour:
                self.traitement_image()

            # update image
            imageTmp = ImageTk.PhotoImage(image=Image.fromarray(self.image.image_cv2))
            self.image.update_image_canvas(imageTmp)
            self.canvas_image.update_idletasks()
            self.canvas_image.update()
            sleep(0.01)

    def traitement_image(self):
        # colors
        image_colorless = Image_Builder(self.image.image_cv2) \
            .extract_image_range_color(self.menu.slider_get_min_color(),
                                       self.menu.slider_get_max_color()) \
            .image

        image_contours_raw = Image_Builder(self.image.image_cv2.copy()) \
            .extract_contours(self.menu.slider_contour.get()) \
            .draw_contours(image=Image_Builder(image_colorless, image_type="black").image) \
            .image

        # logo losange rouge
        image_contours_approximate_rouge = Image_Builder(self.image.image_cv2) \
            .extract_image_range_color((self.menu.slider_get_min_color()),
                                       self.menu.slider_get_max_color()) \
            .extract_contours(self.menu.slider_contour.get()) \
            .approximate_contours(lambda image_builder, contour:
                                  image_builder.approximate_contour_polygon_pointes(
                                      self.menu.slider_contour_precision.get(),
                                      contour,
                                      return_contour=True)) \
            .filter_contours_polygon(peak=self.menu.slider_peak.get()) \
            .extract_contour(position=self.menu.slider_position.get()) \
            .draw_contour(color=(0, 0, 255), image=Image_Builder(image_colorless, image_type="black").image) \
            .draw_contour_line(color=(0, 0, 255)) \
            .extract_inside_contour_from_contour() \
            .draw_contour(color=(0, 255, 0)) \
            .draw_contour_line(color=(0, 255, 0)) \
            .image

        # logo carré orange
        image_contours_approximate_orange = Image_Builder(self.image.image_cv2) \
            .extract_image_range_color((96, 185, 110),
                                       (114, 255, 255)) \
            .extract_contours(50) \
            .approximate_contours(lambda image_builder, contour:
                                  image_builder.approximate_contour_polygon_pointes(
                                      70,
                                      contour,
                                      return_contour=True)) \
            .filter_contours_polygon(peak=4) \
            .extract_contour(position=self.menu.slider_position.get()) \
            .draw_contour(color=(0, 0, 255), image=Image_Builder(image_colorless, image_type="black").image) \
            .draw_contour_line(color=(0, 0, 255)) \
            .image

        image_contours_approximate = cv2.add(image_contours_approximate_rouge, image_contours_approximate_orange)

        # mode d'affichage
        mode = self.menu.slider_mode_affichage.get()
        if mode == 0:
            # affichage image brut + contours
            self.image.image_cv2 = Image_Builder(self.image.image_cv2) \
                .add_image(image_contours_approximate).image
        elif mode == 1:
            # affichage objet + contours
            self.image.image_cv2 = Image_Builder(image_colorless) \
                .add_image(image_contours_approximate).image
        elif mode == 2:
            # affichage contours
            self.image.image_cv2 = image_contours_approximate
        else:
            # affichage des contours bruts
            self.image.image_cv2 = image_contours_raw
