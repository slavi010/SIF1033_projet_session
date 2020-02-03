import tkFileDialog as tkfd


class File:
    def __init__(self):
        pass

    @staticmethod
    def get_file(root, file_types, title):
        # return tkfd.askopenfile(parent=root mode='r', filetypes=[("PNG", "*.png")], title='Choose an excel file')
        return tkfd.askopenfile(parent=root, mode='r', filetypes=file_types, title=title)

    @staticmethod
    def get_image(root):
        return File.get_file(root, [("PNG", "*.png"), ("JPEG", "*.jpg")], "Choisissez une image").name
