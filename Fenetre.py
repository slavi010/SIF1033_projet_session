import Tkinter as tk
from File import File
import cv2 as cv2
from PIL import Image, ImageTk


# root.mainloop()

class Fenetre:
    root = None

    def __init__(self):
        self.root = tk.Tk()
        self.init_menubar()
        # self.show_image()

    def init_menubar(self):
        # toplevel menu
        menubar = tk.Menu(self.root)

        # fichier sous-menu
        fichier_menu = tk.Menu(self.root, tearoff=0)
        # ouvrir une image
        fichier_menu.add_command(label="Ouvrir une image", command=self.show_image)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)

        # display the menu
        self.root.config(menu=menubar)

    def show_image(self, image_path=None):
        if image_path == None:
            image_path = File.get_image(self.root)

        image_cv2 = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

        height, width, no_channels = image_cv2.shape
        image = ImageTk.PhotoImage(image=Image.fromarray(image_cv2))

        canvas = tk.Canvas(self.root, width=width, height=height)
        canvas.pack()
        canvas.create_image(0, 0, image=image, anchor=tk.NW)
        self.root.update_idletasks()
        self.root.update()