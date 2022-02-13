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
            "s_precision": "Accuracy",
            "s_peak": "Number of peak",
            "m_mode": "View mode",
            "m_file": "File",
            "m_oimg": "Open an image",
        }


        self.fenetre = fenetre

        # fenetre des slider
        self.root_slider = tk.Tk()

        # barre de menu
        self.menubar = tk.Menu(self.fenetre.root)
        self.init_menubar()
        self.outils_contour = False

        # slider
        self.nb_slider = 0

        self.slider = {
            # color HSV lower and upper
            "s_h1": self.init_slider(0, label=self.labels.get("s_h1")),
            "s_s1": self.init_slider(0, label=self.labels.get("s_s1")),
            "s_v1": self.init_slider(0, label=self.labels.get("s_v1")),
            "s_h2": self.init_slider(255, label=self.labels.get("s_h2")),
            "s_s2": self.init_slider(255, label=self.labels.get("s_s2")),
            "s_v2": self.init_slider(255, label=self.labels.get("s_v2")),
            # contours
            "s_thresh": self.init_slider(25, label=self.labels.get("s_thresh")),
            "s_precision": self.init_slider(45, min=0, max=1000, label=self.labels.get("s_precision")),
            "s_peak": self.init_slider(4, min=0, max=20, label=self.labels.get("s_peak")),
        }

        # mode d'affichage
        self.mode = 0
        self.show_image = 0

        self.callback_affichage(0)
        self.callback_image(0)



    def init_menubar(self):
        # toplevel menu

        # fichier sous-menu
        fichier_menu = tk.Menu(self.fenetre.root, tearoff=0)
        # ouvre l'image de test
        fichier_menu.add_command(label="Open the sample image", command=lambda : self.callback_open_image(image_path='./image/image_produits_toxiques.jpg'))
        # ouvrir une image
        fichier_menu.add_command(label="Open an image", command=self.callback_open_image)
        # ouvrir flux video
        fichier_menu.add_command(label="Open the cam", command=self.callback_video)
        self.menubar.add_cascade(label="File", menu=fichier_menu)

        # affichage sous-menu
        image_menu = tk.Menu(self.fenetre.root, tearoff=0)
        image_menu.add_command(label="Original image + contours", command=lambda: self.callback_affichage(0))
        image_menu.add_command(label="partial image + contours", command=lambda: self.callback_affichage(1))
        image_menu.add_command(label="Contours", command=lambda: self.callback_affichage(2))
        image_menu.add_command(label="Partial image + ROI", command=lambda: self.callback_affichage(3))
        image_menu.add_command(label="ROI", command=lambda: self.callback_affichage(4))
        self.menubar.add_cascade(label="View", menu=image_menu)

        # Objet sous-menu
        objet_menu = tk.Menu(self.fenetre.root, tearoff=0)
        objet_menu.add_command(label="Actual version (red diamond)", command=lambda: self.callback_image(0))
        objet_menu.add_command(label="Older version (square orange)", command=lambda: self.callback_image(1))
        self.menubar.add_cascade(label="Type of pictograms", menu=objet_menu)

        result_menu = tk.Menu(self.fenetre.root, tearoff=0)
        self.menubar.add_cascade(label="Number of detected pictograms : 0", menu=result_menu)


    # display the menu
        self.fenetre.root.config(menu=self.menubar)

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

    def slider_set(self, values=None):
        if values is None:
            values = {}
        for key in values.keys():
            self.slider.get(key).set(values.get(key))

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

    def callback_open_image(self, image_path=None):
        self.fenetre.show_image(image_path=image_path)

    def callback_video(self):
        self.fenetre.show_image(camera=True)

    def callback_affichage(self, mode=0):
        self.mode = mode

        if mode == 3 or mode == 4:
            self.slider_enable_all()
            self.slider_disable(self.slider.get("s_precision"))
            self.slider_disable(self.slider.get("s_peak"))
            self.slider_disable(self.slider.get("s_position"))

        else:
            self.slider_enable_all()

    def callback_image(self, mode):
        self.show_image = mode

        if mode == 0:
            self.slider_set({
                "s_h1": 108,
                "s_s1": 35,
                "s_v1": 0,
                "s_h2": 145,
                "s_s2": 255,
                "s_v2": 255,
                "s_thresh": 25,
                "s_precision": 45,
                "s_peak": 4,
            })
        else:
            self.slider_set({
                "s_h1": 96,
                "s_s1": 185,
                "s_v1": 110,
                "s_h2": 114,
                "s_s2": 255,
                "s_v2": 255,
                "s_thresh": 50,
                "s_precision": 70,
                "s_peak": 4,
            })

    def set_number_result(self, number):
        if number > 0:
            self.menubar.entryconfigure(4, label="/!\\ Number of detected pictograms : " + str(number) + " /!\\")
        else:
            self.menubar.entryconfigure(4, label="No detected pictogram")
