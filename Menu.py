import Tkinter as tk


class Menu:
    def __init__(self, fenetre):
        self.fenetre = fenetre

        # fenetre des slider
        self.root_slider = tk.Tk()

        # barre de menu
        self.init_menubar()
        self.outils_contour = False

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
        self.slider_contour = self.init_slider(25, label="Contour thresh")
        self.slider_contour_precision = self.init_slider(45, min=0, max=1000, label="Contour precision")
        self.slider_peak = self.init_slider(4, min=0, max=20, label="Nombre de sommet")
        self.slider_position = self.init_slider(0, min=0, max=10, label="Position")
        self.slider_mode_affichage = self.init_slider(0, min=0, max=3, label="Mode d'affichage")


    def init_menubar(self):
        # toplevel menu
        menubar = tk.Menu(self.fenetre.root)

        # fichier sous-menu
        fichier_menu = tk.Menu(self.fenetre.root, tearoff=0)
        # ouvrir une image
        fichier_menu.add_command(label="Ouvrir une image", command=self.callback_open_image)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)

        # image sous-menu
        image_menu = tk.Menu(self.fenetre.root, tearoff=0)
        # contour de l'image
        image_menu.add_command(label="Contour de l'image", command=self.callback_outils_contour)
        menubar.add_cascade(label="Outils", menu=image_menu)

        # display the menu
        self.fenetre.root.config(menu=menubar)

    def init_slider(self, default=100, min=0, max=255, label=""):
        w = tk.Scale(self.root_slider, from_=min, to=max, orient=tk.HORIZONTAL, length=300)
        lbl = tk.Label(self.root_slider , text=label)
        lbl.grid(row=self.nb_slider, column=0)
        w.grid(row=self.nb_slider, column=1)
        w.set(default)
        self.nb_slider += 1
        return w

    # min HSV
    def slider_get_min_color(self):
        return (self.slider_h1.get(),
                self.slider_s1.get(),
                self.slider_v1.get())

    # min HSV
    def slider_get_max_color(self):
        return (self.slider_h2.get(),
                self.slider_s2.get(),
                self.slider_v2.get())

    def callback_open_image(self):
        self.fenetre.show_image()

    def callback_outils_contour(self):
        self.outils_contour = not self.outils_contour

