import Tkinter as tk


class Menu:
    def __init__(self, fenetre):
        self.labels = {
            "s_h1": "Min H",
            "s_s1": "Min S",
            "s_v1": "Min V",
            "s_h2": "Max H",
            "s_s2": "Max S",
            "s_v2": "Max V",
            "s_thresh": "Contour thresh",
            "s_precision": "Precision",
            "s_peak": "Nombre de sommet",
            "s_position": "Position",
            "m_mode": "Mode d'affichage",
            "m_file": "Fichier",
            "m_oimg": "Ouvrir une image",
        }


        self.fenetre = fenetre

        # fenetre des slider
        self.root_slider = tk.Tk()

        # barre de menu
        self.init_menubar()
        self.outils_contour = False

        # slider
        self.nb_slider = 0

        self.slider = {
            # color HSV lower and upper
            "s_h1": self.init_slider(108, label=self.labels.get("s_h1")),
            "s_s1": self.init_slider(38, label=self.labels.get("s_s1")),
            "s_v1": self.init_slider(0, label=self.labels.get("s_v1")),
            "s_h2": self.init_slider(133, label=self.labels.get("s_h2")),
            "s_s2": self.init_slider(255, label=self.labels.get("s_s2")),
            "s_v2": self.init_slider(255, label=self.labels.get("s_v2")),
            # contours
            "s_thresh": self.init_slider(25, label=self.labels.get("s_thresh")),
            "s_precision": self.init_slider(45, min=0, max=1000, label=self.labels.get("s_precision")),
            "s_peak": self.init_slider(4, min=0, max=20, label=self.labels.get("s_peak")),
            "s_position": self.init_slider(0, min=0, max=10, label=self.labels.get("s_position")),
        }

        # mode d'affichage
        self.mode = 0
        self.show_image = 0

        self.callback_affichage(0)



    def init_menubar(self):
        # toplevel menu
        menubar = tk.Menu(self.fenetre.root)

        # fichier sous-menu
        fichier_menu = tk.Menu(self.fenetre.root, tearoff=0)
        # ouvrir une image
        fichier_menu.add_command(label="Ouvrir une image", command=self.callback_open_image)
        # ouvrir flux video
        fichier_menu.add_command(label="Ouvrir la camera", command=self.callback_video)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)

        # affichage sous-menu
        image_menu = tk.Menu(self.fenetre.root, tearoff=0)
        image_menu.add_command(label="Image originale + contours", command=lambda: self.callback_affichage(0))
        image_menu.add_command(label="Image partielle + contours", command=lambda: self.callback_affichage(1))
        image_menu.add_command(label="Contours", command=lambda: self.callback_affichage(2))
        image_menu.add_command(label="ROI", command=lambda: self.callback_affichage(3))
        menubar.add_cascade(label="Affichage", menu=image_menu)

        # image sous-menu
        image_menu = tk.Menu(self.fenetre.root, tearoff=0)
        image_menu.add_command(label="Personalise", command=lambda: self.callback_image(0))
        image_menu.add_command(label="Orange", command=lambda: self.callback_image(1))
        menubar.add_cascade(label="Image", menu=image_menu)

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

    def slider_disable(self, slider):
        slider.config(state='disabled', background='gray63')

    def slider_disable_all(self):
        for s in self.slider.values():
            self.slider_disable(s)

    def slider_enable(self, slider):
        slider.config(state='normal', background='gray94')

    def slider_enable_all(self):
        for s in self.slider.values():
            self.slider_enable(s)

    # min HSV
    def slider_get_min_color(self):
        return (self.slider.get("s_h1").get(),
                self.slider.get("s_s1").get(),
                self.slider.get("s_v1").get())

    # min HSV
    def slider_get_max_color(self):
        return (self.slider.get("s_h2").get(),
                self.slider.get("s_s2").get(),
                self.slider.get("s_v2").get())

    def callback_open_image(self):
        self.fenetre.show_image()

    def callback_video(self):
        self.fenetre.show_image(camera=True)

    def callback_affichage(self, mode=0):
        self.mode = mode

        if mode == 3:
            self.slider_disable_all()
            self.slider_enable(self.slider.get("s_thresh"))
        else:
            self.slider_enable_all()

    def callback_image(self, mode):
        self.show_image = mode
