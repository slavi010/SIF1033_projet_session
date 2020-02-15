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
    def resize(self, new_width, new_height):
        height, width, no_channels = self.start_image_cv2.shape
        self.image_cv2 = cv2.resize(self.start_image_cv2, (new_width, new_height))
        self.start_image_cv2 = self.image_cv2











    def to_contour(self, value, mode_affichage, contour_precision):
        ret, thresh = cv2.threshold(cv2.cvtColor(self.image_cv2.copy(), cv2.COLOR_BGR2GRAY), value, 255,
                                    cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        if len(contours) > 0:
            area = cv2.contourArea(contours[0])


        # recherche de l'objet le plus probable
        contour_object = None
        for c in contours:
            # approximate the contour

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if contour_object is None:
                approx = cv2.convexHull(c)
                peri = cv2.arcLength(approx, True)
                approx = cv2.approxPolyDP(approx, contour_precision/1000.0 * peri, True)
                contour_object = approx
                break


        image_contour = np.zeros_like(self.image_cv2)
        cv2.drawContours(image_contour, contour_object, -1, (0, 255, 0), 3)

        if contour_object is not None:
            for i in range(len(contour_object)):
                for j in range(i, len(contour_object)):
                    lineThickness = 2
                    cv2.line(image_contour, (contour_object[i][0][0], contour_object[i][0][1]),
                             (contour_object[j][0][0], contour_object[j][0][1]), (0, 255, 0), lineThickness)

        if mode_affichage == 0:  # affichage image brut + contours
            self.image_cv2 = cv2.add(self.start_image_cv2, image_contour)
        elif mode_affichage == 1:  # affichage objet + contours
            self.image_cv2 = cv2.add(self.image_cv2, image_contour)
        else:  # affichage contours
            self.image_cv2 = image_contour

        # mask = cv2.inRange(cv2.cvtColor(self.image_cv2, cv2.COLOR_BGR2HSV), (value, 0, 0), (value + 30, 255, 255))
        # mask = cv2.erode(mask, None, iterations=2)
        # mask = cv2.dilate(mask, None, iterations=2)
        #
        # self.image_cv2 = mask.copy()

    def inRange(self, h1, s1, v1, h2, s2, v2):
        mask = cv2.inRange(cv2.cvtColor(self.image_cv2, cv2.COLOR_BGR2HSV), (h1, s1, v1), (h2, s2, v2))
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        self.image_cv2 = cv2.bitwise_and(self.start_image_cv2, self.start_image_cv2, mask=mask)