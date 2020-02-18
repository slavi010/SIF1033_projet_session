import cv2
import numpy as np


class Image_Builder:
    def __init__(self, image, image_type="default"):
        # RGB - cv2
        if image_type == "black":
            self.image = np.zeros_like(image)
        else:
            self.image = image
        self.contours = None
        self.contour = None

    def extract_image_range_color(self, min_color=(0, 0, 0), max_color=(255, 255, 255)):
        # couleurs en HSV
        mask = cv2.inRange(cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV), min_color, max_color)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        self.image = cv2.bitwise_and(self.image, self.image, mask=mask)
        return self

    def extract_contours(self, value=10, min_area=1000):
        ret, thresh = cv2.threshold(cv2.cvtColor(self.image.copy(),
                                                 cv2.COLOR_BGR2GRAY),
                                    value,
                                    255,
                                    cv2.THRESH_BINARY)
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        self.contours = sorted(self.contours, key=cv2.contourArea, reverse=True)
        for i in range(len(self.contours)):
            if cv2.contourArea(self.contours[i]) < min_area:
                self.contours = self.contours[:i]
                break
        return self

    def filter_contours_polygon(self, peak=4):
        result = []
        for i in range(len(self.contours)):
            if len(self.contours[i]) == peak:
                result.append(self.contours[i])
        self.contours = result
        return self

    def extract_contour(self, position=0):
        if self.contours is not None and len(self.contours) > position:
            self.contour = self.contours[position]
        return self

    def extract_inside_contour_from_contour(self):

        if self.contour is not None:
            minmax_current = self.get_min_max_xy_from_contour(self.contour)

            for c in self.contours:
                minmax_temp = self.get_min_max_xy_from_contour(c)
                if minmax_current[0] < minmax_temp[0] and \
                        minmax_current[1] > minmax_temp[1] and \
                        minmax_current[2] < minmax_temp[2] and \
                        minmax_current[3] > minmax_temp[3]:
                    self.contour = c
                    return self
        self.contour = None
        return self

    def approximate_contour_polygon_pointes(self, precision, contour=None, return_contour=False):
        if contour is None:
            contour = self.contour

        if contour is not None:
            peri = cv2.arcLength(contour, True)
            contour = cv2.approxPolyDP(contour, precision/1000.0 * peri, True)

        if return_contour:
            return contour
        return self

    def approximate_contour_convexhull(self, contour=None, return_contour=False):
        if contour is None:
            contour = self.contour
        if contour is not None:
            contour = cv2.convexHull(contour)

        if return_contour:
            return contour
        return self

    def approximate_contours(self, lambda_exp):
        for i in range(len(self.contours)):
            self.contours[i] = lambda_exp(self, self.contours[i])
        return self

    def draw_contours(self, color=(0, 255, 0), image=None):
        if self.contours is not None:
            if image is not None:
                self.image = cv2.drawContours(image, self.contours, -1, color, 3)
            else:
                cv2.drawContours(self.image, self.contours, -1, color, 3)
        if image is not None:
            self.image = image
        return self

    def draw_contour(self, color=(0, 255, 0), image=None):
        if self.contour is not None:
            if image is not None:
                self.image = cv2.drawContours(image, self.contour, -1, color, 3)
            else:
                cv2.drawContours(self.image, self.contour, -1, color, 3)
        if image is not None:
            self.image = image
        return self

    def add_image(self, image):
        if image is not None:
            self.image = cv2.add(self.image, image)
        return self

    def apply_filter_gaussian_blur(self, size=(3, 3)):
        self.image = cv2.GaussianBlur(self.image, size, 0)
        return self

    # private function
    def get_min_max_xy_from_contour(self, contour):
        min_x = 999999
        max_x = 0
        min_y = 999999
        max_y = 0
        for point in contour:
            if point[0][0] < min_x:
                min_x = point[0][0]
            if point[0][0] > max_x:
                max_x = point[0][0]
            if point[0][1] < min_y:
                min_y = point[0][1]
            if point[0][1] > max_y:
                max_y = point[0][1]

        return [min_x, max_x, min_y, max_y]

    def print_contour(self):
        print self.contour
        return self

    def draw_contour_line(self, color=(0, 255, 0), image=None, contour=None):
        if image is None:
            image = self.image
        if contour is None:
            contour = self.contour
        if contour is not None:
            for i in range(len(contour)):
                for j in range(i, len(contour)):
                    lineThickness = 2
                    cv2.line(image, (contour[i][0][0], contour[i][0][1]),
                             (contour[j][0][0], contour[j][0][1]), color, lineThickness)
        return self
