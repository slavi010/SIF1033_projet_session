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

class Fenetre:

    def __init__(self):
        # fenetre de l'image
        self.root = tk.Tk()

        # fenetre des slider
        self.root_slider = tk.Tk()

        # canvas de l'image
        self.canvas_image_WIDTH = 1280
        self.canvas_image_HEIGHT = 720

        self.canvas_image = tk.Canvas(
            self.root,
            width=self.canvas_image_WIDTH,
            height=self.canvas_image_HEIGHT)
        self.canvas_image.grid(row=0, column=0)

        self.image = Image_canvas(self.canvas_image)

        # FigureCanvasTkAgg()

        # barre de menu
        self.init_menubar()
        self.isContourActivated = False

        # slider
        self.nb_slider = 0
        # color HSV lower and upper
        self.slider_h1 = self.init_slider(108, label="Min H")
        self.slider_s1 = self.init_slider(38, label="Min S")
        self.slider_v1 = self.init_slider(0, label="Min V")
        self.slider_h2 = self.init_slider(133, label="Max H")
        self.slider_s2 = self.init_slider(225, label="Max S")
        self.slider_v2 = self.init_slider(255, label="Max V")
        # contours
        self.slider_contour = self.init_slider(25, label="Contour")
        self.slider_contour_precision = self.init_slider(45, min=0, max=1000, label="Contour precision")
        self.slider_peak = self.init_slider(4, min=0, max=20, label="Nombre de sommet")
        self.slider_position = self.init_slider(0, min=0, max=10, label="Position")
        self.slider_mode_affichage = self.init_slider(0, min=0, max=2, label="Mode d'affichage")

    def init_menubar(self):
        # toplevel menu
        menubar = tk.Menu(self.root)

        # fichier sous-menu
        fichier_menu = tk.Menu(self.root, tearoff=0)
        # ouvrir une image
        fichier_menu.add_command(label="Ouvrir une image", command=self.show_image)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)

        # image sous-menu
        image_menu = tk.Menu(self.root, tearoff=0)
        # contour de l'image
        image_menu.add_command(label="Contour de l'image", command=self.menu_contour)
        menubar.add_cascade(label="Outils", menu=image_menu)

        # display the menu
        self.root.config(menu=menubar)

    def init_slider(self, default=100, min=0, max=255, label=""):
        w = tk.Scale(self.root_slider, from_=min, to=max, orient=tk.HORIZONTAL, length=300)
        lbl = tk.Label(self.root_slider , text=label)
        lbl.grid(row=self.nb_slider, column=0)
        w.grid(row=self.nb_slider, column=1)
        w.set(default)
        self.nb_slider += 1
        return w

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

            if self.isContourActivated:
                self.traitement_image()

            # update image
            imageTmp = ImageTk.PhotoImage(image=Image.fromarray(self.image.image_cv2))
            self.image.update_image_canvas(imageTmp)
            self.canvas_image.update_idletasks()
            self.canvas_image.update()
            sleep(0.01)

    def menu_contour(self):
        self.isContourActivated = not self.isContourActivated
        if self.image.image_cv2 is not None:
            self.traitement_image()

    def traitement_image(self):
        # colors
        min_color = (self.slider_h1.get(),
                     self.slider_s1.get(),
                     self.slider_v1.get())
        max_color = (self.slider_h2.get(),
                     self.slider_s2.get(),
                     self.slider_v2.get())

        image_colorless = Image_Builder(self.image.image_cv2) \
            .extract_image_range_color(min_color, max_color) \
            .image

        image_contours = Image_Builder(image_colorless) \
            .extract_contours(self.slider_contour.get()) \
            .approximate_contours(lambda image_builder, contour:
                                  image_builder.approximate_contour_polygon_pointes(
                                      self.slider_contour_precision.get(),
                                      contour,
                                      return_contour=True)) \
            .extract_contour_polygon(position=self.slider_position.get(), peak=self.slider_peak.get()) \
            .draw_contour(color=(0, 0, 255), image=Image_Builder(image_colorless, image_type="black").image) \
            .draw_contour_line(color=(0, 0, 255)) \
            .extract_inside_contour_from_contour() \
            .draw_contour(color=(0, 255, 0)) \
            .draw_contour_line(color=(0, 255, 0)) \
            .image

        # mode d'affichage
        mode = self.slider_mode_affichage.get()
        if mode == 0:
            # affichage image brut + contours
            self.image.image_cv2 = Image_Builder(self.image.image_cv2) \
                .add_image(image_contours).image
        elif mode == 1:
            # affichage objet + contours
            self.image.image_cv2 = Image_Builder(image_colorless) \
                .add_image(image_contours).image
        else:
            # affichage contours
            self.image.image_cv2 = image_contours

